%define pgprefix %{_usr}/local/openresty/postgresql
%define pg_config %{pgprefix}/bin/pg_config
%define ext orsl

Name:       openresty-postgresql-%{ext}
Version:    0.01
Release:    1%{?dist}
Summary:    PostgreSQL extension contains utilities used in mini-sl
Group:      Applications/System
License:    BSD
URL:        https://github.com/
Source0:    postgres-orsl-%{version}.tar.gz

BuildRequires:  openresty-postgresql-devel >= 9.6.8
Requires:       openresty-postgresql >= 9.6.8

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/postgres-%{ext}-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%description
PostgreSQL extension contains utilities used in mini-sl

%prep
%setup -q -n postgres-%{ext}-%{version}

%build
make %{?_smp_mflags} PG_CONFIG=%{pg_config}

%install
make install DESTDIR=${RPM_BUILD_ROOT} PG_CONFIG=%{pg_config}

%clean
rm -fr $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%{pgprefix}/share/extension/%{ext}*.sql
%{pgprefix}/share/extension/%{ext}.control
%{pgprefix}/lib/%{ext}.so

%changelog
* Thu Jul 4 2018 Yichun Zhang 0.01
- initial build for openresty-orsl.
