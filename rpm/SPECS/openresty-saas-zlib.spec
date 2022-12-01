Name:               openresty-saas-zlib
Version:            1.2.13
Release:            1%{?dist}
Summary:            The zlib compression library for OpenResty SaaS

Group:              System Environment/Libraries

# /contrib/dotzlib/ have Boost license
License:            zlib and Boost
URL:                http://www.zlib.net/
Source0:            http://www.zlib.net/zlib-%{version}.tar.xz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      libtool

AutoReqProv:        no

%define zlib_prefix     /opt/openresty-saas/zlib


%description
The zlib compression library for use by Openresty SaaS ONLY


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/zlib-%{version}"; \
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


%package devel

Summary:            Development files for OpenResty SaaS's zlib library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty SaaS's zlib library.


%prep
%setup -q -n zlib-%{version}


%build
./configure --prefix=%{zlib_prefix}
make -j`nproc` CFLAGS='-O2 -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    SFLAGS='-O2 -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    > /dev/stderr


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{zlib_prefix}/share
rm -f  %{buildroot}/%{zlib_prefix}/lib/*.la
rm -rf %{buildroot}/%{zlib_prefix}/lib/pkgconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%dir %{zlib_prefix}
%dir %{zlib_prefix}/lib
%attr(0755,root,root) %{zlib_prefix}/lib/libz.so*


%files devel
%defattr(-,root,root,-)

%dir %{zlib_prefix}/include
%{zlib_prefix}/lib/*.a
%{zlib_prefix}/include/zlib.h
%{zlib_prefix}/include/zconf.h


%changelog
* Wed Nov 30 2022 Yichun Zhang (agentzh) 1.2.13-1
- upgraded PCRE to 1.2.13.
* Thu Mar 31 2022 Yichun Zhang (agentzh) 1.2.12-1
- upgraded zlib to 1.2.12.
* Wed May 27 2020 Johnny Wang 1.2.11-1
- initial build for zlib-saas 1.2.11.
