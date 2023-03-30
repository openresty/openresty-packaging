Name:               openresty-hiredis
Version:            1.0.3.3
Release:            2%{?dist}
Summary:            The hiredis library for OpenResty

Group:              System Environment/Libraries

License:            BSD 3-Clause "New" or "Revised" License
URL:                https://github.com/redis/hiredis
Source0:            hiredis-plus-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openresty-plus-openssl111-devel >= 1.1.1l-1

Requires:       openresty-plus-openssl111 >= 1.1.1l-1

AutoReqProv:        no

%define openssl_prefix     /usr/local/openresty-plus/openssl111
%define hiredis_prefix     /usr/local/openresty-plus/hiredis


%description
The hiredis library for use by OpenResty ONLY

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/hiredis-plus-%{version}"; \
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

Summary:            Development files for OpenResty's hiredis library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and library for OpenResty's hiredis library.


%prep
%setup -q -n hiredis-plus-%{version}


%build
make -j`nproc` USE_SSL=1 PREFIX=%{hiredis_prefix} \
    OPENSSL_PREFIX=%{openssl_prefix} \
    CFLAGS='-DHIREDIS_USE_FREE_LISTS' \
    V=1


%install
make install USE_SSL=1 PREFIX=%{hiredis_prefix} DESTDIR=%{buildroot}
rm -f  %{buildroot}/%{hiredis_prefix}/lib/*.a
rm -rf %{buildroot}/%{hiredis_prefix}/lib/pkgconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{hiredis_prefix}/lib/libhiredis.so*
%attr(0755,root,root) %{hiredis_prefix}/lib/libhiredis_ssl.so*


%files devel
%defattr(-,root,root,-)

%{hiredis_prefix}/include/hiredis/*.h
%{hiredis_prefix}/include/hiredis/adapters/*.h


%changelog
* Thu Mar 30 2023 Yichun Zhang (agentzh) 1.0.3.3-1
- upgraded openresty-hiredis to 1.0.3.3.
* Fri Mar 11 2022 Yichun Zhang (agentzh) 1.0.3.2-1
- upgraded openresty-hiredis to 1.0.3.2.
* Mon Feb 07 2022 Yichun Zhang 1.0.3.1
- initial version
