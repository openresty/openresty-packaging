%define pgprefix %{_usr}/local/openresty/postgresql
%define pg_config %{pgprefix}/bin/pg_config
%define ext orsl

Name:       openresty-postgresql-%{ext}
Version:    0.02
Release:    4%{?dist}
Summary:    PostgreSQL extension contains utilities used in mini-sl
Group:      Productivity/Database
License:    BSD
URL:        https://github.com/
Source0:    postgres-orsl-%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  openresty-postgresql-devel >= 9.6.8
Requires:       openresty-postgresql >= 9.6.8


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
make -j`nproc` PG_CONFIG=%{pg_config}


%install
make install DESTDIR=${RPM_BUILD_ROOT} PG_CONFIG=%{pg_config}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -fr $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%{pgprefix}/share/extension/%{ext}*.sql
%{pgprefix}/share/extension/%{ext}.control
%{pgprefix}/lib/%{ext}.so

%changelog
* Thu Aug 13 2020 Yichun Zhang (agentzh) 0.02-1
- upgraded postgres-orsl to 0.02.
* Thu Jul 4 2018 Yichun Zhang 0.01
- initial build for openresty-orsl.
