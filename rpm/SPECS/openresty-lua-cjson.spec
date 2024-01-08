Name:               openresty-lua-cjson
Version:            2.1.0.13.2
Release:            1%{?dist}
Summary:            The lua-cjson library for OpenResty

Group:              System Environment/Libraries

License:            MIT
URL:                https://github.com/orinc/lua-cjson-plus/
Source0:            lua-cjson-plus-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      libtool

AutoReqProv:        no

%define cjson_prefix     /usr/local/openresty/lua-cjson


%description
The cjson compression library for use by OpenResty ONLY

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-cjson-plus-%{version}"; \
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
%setup -q -n lua-cjson-plus-%{version}


%build
export LUA_INCLUDE_DIR=/usr/local/openresty/luajit/include/luajit-2.1/
export LUA_LIBRARY=/usr/local/openresty/luajit/lib/
SHELL="bash -x" make VERBOSE=1


%install
install -d %{buildroot}%{cjson_prefix}/lib
install -m 0755 cjson.so %{buildroot}%{cjson_prefix}/lib


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{cjson_prefix}/lib/cjson.so



%changelog
* Mon Jan 8 2024 Yichun Zhang (agentzh) 2.1.0.13.2-1
- upgraded lua-cjson-plus to 2.1.0.13.2.
* Mon Apr 17 2023 Yichun Zhang (agentzh) 2.1.0.12.1

- upgraded lua-cjson 2.1.0.12.1
