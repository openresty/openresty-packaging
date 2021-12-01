Name:           openresty-libedge-pki
Version:        1.1.5
Release:        1%{?dist}
Summary:        OpenResty Edge Certificates C Library

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

Source0:        edge-pki-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel

AutoReqProv:        no

%define or_prefix                       %{_usr}/local/openresty-plus
%define lua_lib_dir                     %{or_prefix}/lualib


%description
Lua API for generating/verifying edge certificates.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/edge-pki-%{version}"; \
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
%setup -q -n "edge-pki-%{version}"


%build
make


%install
rm -rf %{buildroot}
make install_c DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%{lua_lib_dir}/libedgepki.so


%changelog
* Wed Dec 1 2021 Yichun Zhang (agentzh) 1.1.5-1
- upgraded openresty-libedge-pki to 1.1.5.
* Thu Nov 17 2021 Wang Hui (wanghuizzz) 1.1.4-1
- initial packaging.
