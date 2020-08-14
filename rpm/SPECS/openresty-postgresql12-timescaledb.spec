%define pgprefix %{_usr}/local/openresty-postgresql12
%define pg_config %{pgprefix}/bin/pg_config
%define ext timescaledb

Name:       openresty-postgresql12-%{ext}
Version:    1.7.2
Release:    1%{?dist}
Summary:    TimescaleDB PostgreSQL extension
Group:      Productivity/Database
License:    BSD
URL:        https://github.com/timescale/timescaledb
Source0:    https://github.com/timescale/timescaledb/archive/%{version}.tar.gz

BuildRequires:  openresty-postgresql12-devel >= 12.3
Requires:       openresty-postgresql12 >= 12.3

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{ext}-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%description
Open-source PostgreSQL extension designed to make SQL scalable for time-series data.

%prep
%setup -q -n %{ext}-%{version}

%build
./bootstrap -DPG_CONFIG=%{pg_config} -DREGRESS_CHECKS=OFF -DCMAKE_BUILD_TYPE=RelWithDebInfo
cd build && make %{?_smp_mflags}

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
* Sat Aug 8 2020 LI Geng 1.7.2
- initial build for TimescaleDB on postgresql v12.
