Name:           openresty-wrk
Version:        4.0.2.1
Release:        4%{?dist}
Summary:        The OpenResty fork of wrk

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

Source0:        wrk-plus-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openresty
BuildRequires:  openresty-openssl111-devel
Requires:       openresty
Requires:       openresty-openssl111

AutoReqProv:        no

%define wrk_prefix                      /usr/local/openresty-wrk
%define or_prefix                       /usr/local/openresty
%define openssl_prefix                  /usr/local/openresty/openssl111


%description
wrk - a HTTP benchmarking tool


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/wrk-plus-%{version}"; \
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
# The $PWD is rpmbuild/BUILD
%setup -q -n "wrk-plus-%{version}"


%build
export PATH=%{or_prefix}/luajit/bin:$PATH
make WITH_LUAJIT=%{or_prefix}/luajit WITH_OPENSSL=%{openssl_prefix}


%install
rm -rf %{buildroot}
install -d %{buildroot}%{wrk_prefix}/bin
install -m 0755 wrk %{buildroot}%{wrk_prefix}/bin


# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%{wrk_prefix}/bin/wrk


%changelog
* Thu Oct 9 2024 Wang Hui (wanghuizzz) 4.0.2.1-4
- update the dependency.
* Mon Jan 8 2024 Wang Hui (wanghuizzz) 4.0.2.1-3
- update the dependency.
* Mon Sep 26 2022 Wang Hui (wanghuizzz) 4.0.2.1-2
- update the dependency.
* Thu Sep 22 2022 Wang Hui (wanghuizzz) 4.0.2.1-1
- initial packaging.
