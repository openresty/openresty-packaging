%define pgprefix %{_usr}/local/openresty-postgresql12
%define pg_config %{pgprefix}/bin/pg_config
%define ext orsl

Name:       openresty-postgresql12-%{ext}
Version:    0.02
Release:    3%{?dist}
Summary:    PostgreSQL extension contains utilities used in mini-sl
Group:      Productivity/Database
License:    BSD
URL:        https://github.com/
Source0:    postgres-orsl-%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  openresty-postgresql12-devel >= 12.3
Requires:       openresty-postgresql12 >= 12.3


%description
PostgreSQL extension contains utilities used in mini-sl


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/postgres-%{ext}-%{version}"; \
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
* Sat Aug 8 2020 LI Geng 0.02
- initial build for openresty-orsl on postgresql v12.
