Name:       openresty-yajl
Version:    2.1.0.4
Release:    2%{?dist}
Summary:    Yet Another JSON Library (YAJL) or OpenResty

Group: Development/Libraries
License: Proprietary
URL: http://lloyd.github.com/yajl/

%define _missing_doc_files_terminate_build 0

%define yajl_prefix      %{_usr}/local/openresty-yajl

Source0: yajl-plus-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ccache, cmake, gcc, make
AutoReqProv:        no

%package devel
Summary: Libraries, includes, etc to develop with YAJL
Requires: %{name} = %{version}-%{release}

AutoReqProv:        no

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


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/yajl-plus-%{version}"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%endif

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%if 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%prep
%setup -q -n yajl-plus-%{version}

%build
# NB, we are not using upstream's 'configure'/'make'
# wrapper, instead we use cmake directly to better
# align with Fedora standards
rm -rf build
mkdir build
cd build
export CC='ccache gcc -fdiagnostics-color=always'
cmake -DCMAKE_INSTALL_PREFIX=%{yajl_prefix} ..
make VERBOSE=1 -j`nproc`


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{yajl_prefix}/lib64
pushd $RPM_BUILD_ROOT%{yajl_prefix}/lib64
ln -sf ../lib/*.so* ./
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{yajl_prefix}
%dir %{yajl_prefix}/bin
%dir %{yajl_prefix}/lib
%dir %{yajl_prefix}/lib64

%defattr(-,root,root,-)
%{yajl_prefix}/bin/json_reformat
%{yajl_prefix}/bin/json_verify
%{yajl_prefix}/lib/libyajl.so.2
%{yajl_prefix}/lib/libyajl.so.2.*
%{yajl_prefix}/lib64/libyajl.so.2
%{yajl_prefix}/lib64/libyajl.so.2.*

%files devel
%defattr(-,root,root,-)
%dir %{yajl_prefix}/include
%dir %{yajl_prefix}/include/yajl
%dir %{yajl_prefix}/share
%dir %{yajl_prefix}/share/pkgconfig
%{yajl_prefix}/include/yajl/yajl_common.h
%{yajl_prefix}/include/yajl/yajl_gen.h
%{yajl_prefix}/include/yajl/yajl_parse.h
%{yajl_prefix}/include/yajl/yajl_tree.h
%{yajl_prefix}/include/yajl/yajl_version.h
%{yajl_prefix}/lib/libyajl.so
%{yajl_prefix}/lib64/libyajl.so
%{yajl_prefix}/share/pkgconfig/yajl.pc
%{yajl_prefix}/lib/libyajl_s.a

%changelog
* Mon Sep 21 2020 Yichun Zhang (agentzh) 2.1.0.4-1
- upgraded yajl-plus to 2.1.0.4.
* Sat Mar 28 2020 Yichun Zhang (agentzh) 2.1.0.3-1
- upgraded yajl-plus to 2.1.0.3.
* Thu Jul 4 2019 Yichun Zhang <yichun@openresty.com> - 2.1.0.2-1
- Initial build.
