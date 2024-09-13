%define pgprefix %{_usr}/local/openresty-postgresql12
%define pg_config %{pgprefix}/bin/pg_config
%define ext pg_auto_failover
%define target_name pgautofailover

Name:       openresty-postgresql12-auto-failover
Version:    2.1
Release:    2%{?dist}
Summary:    Postgres extension for automated failover and high-availability
Group:      Productivity/Database
License:    PostgreSQL
URL:        https://github.com/citusdata/pg_auto_failover
Source0:    https://github.com/citusdata/pg_auto_failover/archive/v%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  openresty-postgresql12-devel >= 12.5-13, ccache, ncurses-devel, libxml2-devel, libxslt-devel, readline-devel, make, gcc
Requires:       openresty-postgresql12 >= 12.5-13


%description
pg_auto_failover is an extension and service for PostgreSQL that monitors and manages
automated failover for a Postgres cluster. It is optimized for simplicity and correctness.

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
make %{?_smp_mflags} PG_CONFIG=%{pg_config}

%install
make install DESTDIR=${RPM_BUILD_ROOT} PG_CONFIG=%{pg_config}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -fr $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%{pgprefix}/bin/pg_autoctl
%{pgprefix}/lib/%{target_name}.so
%{pgprefix}/share/extension/%{target_name}*.sql
%{pgprefix}/share/extension/%{target_name}.control


%changelog
* Wed Sep 11 2024 Your Name <your.email@example.com> 2.1-1
- Initial build for pg_auto_failover on PostgreSQL 12
