Name: openresty-yajl
Version: 2.1.0.2
Release: 1%{?dist}
Summary: Yet Another JSON Library (YAJL) or OpenResty

Group: Development/Libraries
License: ISC
URL: http://lloyd.github.com/yajl/

%define _missing_doc_files_terminate_build 0

%define yajl_prefix      %{_usr}/local/openresty-yajl

#
# NB, upstream does not provide pre-built tar.gz downloads. Instead
# they make you use the 'on the fly' generated tar.gz from GITHub's
# web interface
#
# The Source0 for any version is obtained by a URL
#
#   http://github.com/lloyd/yajl/tarball/1.0.7
#
# Which causes a download of a archive named after
# the GIT hash corresponding to the version tag
#
#   eg lloyd-yajl-45a1bdb.tar.gz
#
# NB even though the tar.gz is generated on the fly by GITHub it
# will always have identical md5sum
#
# So for new versions, update 'githash' to match the hash of the
# GIT tag associated with updated 'Version:' field just above
Source0: yajl-plus-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: cmake

%package devel
Summary: Libraries, includes, etc to develop with YAJL
Requires: %{name} = %{version}-%{release}

AutoReqProv:        no

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/yajl-plus-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%description
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

%description devel
Yet Another JSON Library. YAJL is a small event-driven
(SAX-style) JSON parser written in ANSI C, and a small
validating JSON generator.

This sub-package provides the libraries and includes
necessary for developing against the YAJL library

%prep
%setup -q -n yajl-plus-%{version}

%build
# NB, we are not using upstream's 'configure'/'make'
# wrapper, instead we use cmake directly to better
# align with Fedora standards
mkdir build
cd build
%cmake -DCMAKE_INSTALL_PREFIX=%{yajl_prefix} ..
make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README TODO
%{yajl_prefix}/bin/json_reformat
%{yajl_prefix}/bin/json_verify
%{yajl_prefix}/%{_lib}/libyajl.so.2
%{yajl_prefix}/%{_lib}/libyajl.so.2.*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%dir %{yajl_prefix}/include/yajl
%{yajl_prefix}/include/yajl/yajl_common.h
%{yajl_prefix}/include/yajl/yajl_gen.h
%{yajl_prefix}/include/yajl/yajl_parse.h
%{yajl_prefix}/include/yajl/yajl_tree.h
%{yajl_prefix}/include/yajl/yajl_version.h
%{yajl_prefix}/%{_lib}/libyajl.so
%{yajl_prefix}/share/pkgconfig/yajl.pc
%{yajl_prefix}/%{_lib}/libyajl_s.a

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.0.4-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0.4-3
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug  6 2012 Daniel P. Berrange <berrange@redhat.com> - 2.0.4-1
- Update to 2.0.4 release (rhbz #845777)
- Fix License tag to reflect change in 2.0.0 series from BSD to ISC

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Daniel P. Berrange <berrange@redhat.com> - 2.0.1-1
- Update to 2.0.1 release

* Tue May  3 2011 Daniel P. Berrange <berrange@redhat.com> - 1.0.12-1
- Update to 1.0.12 release

* Fri Dec 17 2010 Daniel P. Berrange <berrange@redhat.com> - 1.0.11-1
- Update to 1.0.11 release

* Mon Jan 11 2010 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-3
- Fix ignoring of cflags (rhbz #547500)

* Tue Dec  8 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-2
- Change use of 'define' to 'global'

* Mon Dec  7 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0.7-1
- Initial Fedora package
