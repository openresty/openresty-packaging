%define pgprefix %{_usr}/local/openresty-postgresql12
%define pg_config %{pgprefix}/bin/pg_config
%define ext ip4r

Name:       openresty-postgresql12-%{ext}
Version:    2.4.1
Release:    4%{?dist}
Summary:    IPv4 and IPv4 range index types for PostgreSQL
Group:      Productivity/Database
License:    BSD
URL:        https://github.com/RhodiumToad/ip4r
Source0:    https://github.com/RhodiumToad/ip4r/archive/%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  openresty-postgresql12-devel >= 12.3
Requires:       openresty-postgresql12 >= 12.3


%description
ip4 and ip4r are types that contain a single IPv4 address and a range of
IPv4 addresses respectively. They can be used as a more flexible,
indexable version of the cidr type.


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
make -j`nproc` PG_CONFIG=%{pg_config}


%install
make install DESTDIR=${RPM_BUILD_ROOT} PG_CONFIG=%{pg_config}
rm ${RPM_BUILD_ROOT}/%{pgprefix}/include/server/extension/ip4r/ipr.h

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -fr $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%{pgprefix}/share/doc/extension/README.%{ext}
%{pgprefix}/share/extension/%{ext}*.sql
%{pgprefix}/share/extension/%{ext}.control
%{pgprefix}/lib/%{ext}.so

%changelog
* Sat Aug 8 2020 LI Geng 2.4.1
- initial build for postgresql extension ip4r on postgresql v12.
