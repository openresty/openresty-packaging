%define pgprefix %{_usr}/local/openresty-postgresql12
%define pg_config %{pgprefix}/bin/pg_config
%define ext timescaledb

%define openssl_prefix      %{_usr}/local/openresty-plus/openssl111

Name:       openresty-postgresql12-%{ext}
Version:    1.7.4
Release:    5%{?dist}
Summary:    TimescaleDB PostgreSQL extension
Group:      Productivity/Database
License:    BSD
URL:        https://github.com/timescale/timescaledb
Source0:    https://github.com/timescale/timescaledb/archive/%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  openresty-postgresql12-devel >= 12.4, openresty-plus-openssl111-devel
Requires:       openresty-postgresql12 >= 12.4, openresty-plus-openssl111


%description
Open-source PostgreSQL extension designed to make SQL scalable for time-series data.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{ext}-%{version}"; \
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
%setup -q -n %{ext}-%{version}


%build
./bootstrap -DPG_CONFIG=%{pg_config} -DREGRESS_CHECKS=OFF -DCMAKE_BUILD_TYPE=RelWithDebInfo \
            -DOPENSSL_ROOT_DIR=%{openssl_prefix}
cd build && make -j`nproc`


%install
cd build && make install DESTDIR=${RPM_BUILD_ROOT}


%clean
rm -fr $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%{pgprefix}/share/extension/%{ext}*.sql
%{pgprefix}/share/extension/%{ext}.control
%{pgprefix}/lib/%{ext}*.so


%changelog
* Wed Dec 23 2020 LI Geng 1.7.4
- bump timescaledb version to 1.7.4
* Sat Aug 8 2020 LI Geng 1.7.2
- initial build for TimescaleDB on postgresql v12.
