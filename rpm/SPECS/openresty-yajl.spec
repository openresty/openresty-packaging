Name: openresty-yajl
Version: 2.1.0.2
Release: 1%{?dist}
Summary: Yet Another JSON Library (YAJL) or OpenResty

Group: Development/Libraries
License: ISC
URL: http://lloyd.github.com/yajl/

%define _missing_doc_files_terminate_build 0

%define yajl_prefix      %{_usr}/local/openresty-yajl

Source0: yajl-plus-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: cmake
AutoReqProv:        no

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
rm -rf build
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

%files
%defattr(-,root,root,-)
%{yajl_prefix}/bin/json_reformat
%{yajl_prefix}/bin/json_verify
%{yajl_prefix}/%{_lib}/libyajl.so.2
%{yajl_prefix}/%{_lib}/libyajl.so.2.*

%files devel
%defattr(-,root,root,-)
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
* Thu Jul 4 2019 Yichun Zhang <yichun@openresty.com> - 2.1.0.2-1
- Initial build.
