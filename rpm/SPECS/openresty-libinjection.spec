Name:           openresty-libinjection
Version:        3.10.1
Release:        1%{?dist}
Summary:        Lua module for SQLI tokenizer parser analyzer

Group:          Development/Libraries

License:        BSD
URL:            https://www.openresty.com/

Source0:        openresty-libinjection-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  make
# LuaJIT is required to compile Lua files into byte code
BuildRequires:  openresty-plus

AutoReqProv:        no

%define orprefix                        %{_usr}/local/openresty-plus
%define lua_lib_dir                     %{orprefix}/site/lualib


%description
This package contains the Lua module for check SQLI and XSS attack.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openresty-libinjection-%{version}"; \
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
%setup -q -n "openresty-libinjection-%{version}"


%build
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
make compile


%install
rm -rf %{buildroot}
make install_c DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%{lua_lib_dir}/libinjection.so


%changelog
* Thu Nov 25 2021 Shushen He (isshe) 3.10.1-1
- initial build for openresty-libinjection.
