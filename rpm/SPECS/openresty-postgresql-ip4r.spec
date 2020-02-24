%define pgprefix %{_usr}/local/openresty/postgresql
%define pg_config %{pgprefix}/bin/pg_config
%define ext ip4r

Name:       openresty-postgresql-%{ext}
Version:    2.4.1
Release:    2%{?dist}
Summary:    IPv4 and IPv4 range index types for PostgreSQL
Group:      Productivity/Database
License:    BSD
URL:        https://github.com/RhodiumToad/ip4r
Source0:    https://github.com/RhodiumToad/ip4r/archive/%{version}.tar.gz

BuildRequires:  openresty-postgresql-devel >= 9.6.8
Requires:       openresty-postgresql >= 9.6.8

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
ip4 and ip4r are types that contain a single IPv4 address and a range of
IPv4 addresses respectively. They can be used as a more flexible,
indexable version of the cidr type.

%prep
%setup -q -n %{ext}-%{version}

%build
make %{?_smp_mflags} PG_CONFIG=%{pg_config}

%install
make install DESTDIR=${RPM_BUILD_ROOT} PG_CONFIG=%{pg_config}

%clean
rm -fr $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%{pgprefix}/share/doc/extension/README.%{ext}
%{pgprefix}/share/extension/%{ext}*.sql
%{pgprefix}/share/extension/%{ext}.control
%{pgprefix}/lib/%{ext}.so

%changelog
* Thu Jul 4 2018 Yichun Zhang 2.4.1
- initial build for postgresql ip4r.
