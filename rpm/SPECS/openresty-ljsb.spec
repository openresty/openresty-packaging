Name:       openresty-ljsb
Version:    1.0.0
Release:    1%{?dist}
Summary:    LuaJIT string buffer encoding

Group: Development/Libraries
License: Proprietary
URL: http://github.com/orinc/ljsb

%define _missing_doc_files_terminate_build 0

%define ljsb_prefix      %{_usr}/local/openresty/ljsb

Source0: ljsb-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ccache, cmake, gcc, make
AutoReqProv:        no

%package devel
Summary: Libraries, includes, etc to develop with YAJL
Requires: %{name} = %{version}-%{release}

AutoReqProv:        no

%description
This library encode data into LuaJIT string.buffer encoding format.

%description devel
This library encode data into LuaJIT string.buffer encoding format.

This sub-package provides the libraries and includes
necessary for developing against the YAJL library


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/ljsb-%{version}"; \
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
%setup -q -n ljsb-%{version}

%build
# NB, we are not using upstream's 'configure'/'make'
# wrapper, instead we use cmake directly to better
# align with Fedora standards
rm -rf build
mkdir build
cd build
export CC='ccache gcc -fdiagnostics-color=always'
cmake -DCMAKE_INSTALL_PREFIX=%{ljsb_prefix} ..
make VERBOSE=1 -j`nproc`


%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{ljsb_prefix}/lib64
pushd $RPM_BUILD_ROOT%{ljsb_prefix}/lib64
ln -sf ../lib/*.so* ./
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{ljsb_prefix}
%dir %{ljsb_prefix}/lib
%dir %{ljsb_prefix}/lib64

%defattr(-,root,root,-)
%{ljsb_prefix}/lib/libljsb.so.1
%{ljsb_prefix}/lib/libljsb.so.1.*
%{ljsb_prefix}/lib64/libljsb.so.1
%{ljsb_prefix}/lib64/libljsb.so.1.*

%files devel
%defattr(-,root,root,-)
%dir %{ljsb_prefix}/include
%dir %{ljsb_prefix}/include/ljsb
%dir %{ljsb_prefix}/share
%dir %{ljsb_prefix}/share/pkgconfig
%{ljsb_prefix}/include/ljsb/ljsb_common.h
%{ljsb_prefix}/include/ljsb/ljsb_gen.h
%{ljsb_prefix}/lib/libljsb.so
%{ljsb_prefix}/lib64/libljsb.so
%{ljsb_prefix}/share/pkgconfig/ljsb.pc
%{ljsb_prefix}/lib/libljsb_s.a

%changelog
* Wed May 8 2024 Junlong Li <lijunlong@openresty.com> - 1.0.0-1
- Initial build.
