%define pgprefix %{_usr}/local/openresty-postgresql16
%define pg_config %{pgprefix}/bin/pg_config
%define ext orsl

Name:       openresty-postgresql16-%{ext}
Version:    0.02
Release:    1%{?dist}
Summary:    PostgreSQL extension contains utilities used in mini-sl
Group:      Productivity/Database
License:    Proprietary
URL:        https://github.com/
Source0:    postgres-orsl-%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  openresty-postgresql16-devel >= 16.5
Requires:       openresty-postgresql16 >= 16.5


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
* Mon Nov 18 2024 He Shushen 0.02
- initial build for openresty-orsl on postgresql v16.
