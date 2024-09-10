Name:           lua-resty-limit-traffic-dynamic
Version:        1.0.3
Release:        1%{?dist}
Summary:        limit HTTP request base on the traffic dynamically.

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

Source0:        lua-resty-limit-traffic-dynamic-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openresty >= 1.19.9
BuildRequires:  ccache, gcc, make


AutoReqProv:        no

%define or_prefix          /usr/local/openresty
%define lua_lib_dir        %{or_prefix}/site/lualib


%description
Limit HTTP request base on the traffic dynamically.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-resty-limit-traffic-dynamic-%{version}"; \
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
%setup -q -n "lua-resty-limit-traffic-dynamic-%{version}"

%build
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
for f in `find lib/resty/ -type f -name '*.lua'`; do
    %{or_prefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm $f
done

make -j`nproc`


%install
rm -rf %{buildroot}

sed -i 's|lib/resty/limit/traffic/dynamic/\*.lua|lib/resty/limit/traffic/dynamic/\*.ljbc|g' Makefile
sed -i 's|lib/resty/limit/traffic/dynamic.lua|lib/resty/limit/traffic/dynamic.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{or_prefix}/site/lualib/resty/limit/traffic/dynamic.ljbc
%{or_prefix}/site/lualib/resty/limit/traffic/dynamic/*.ljbc
%{or_prefix}/site/lualib/*.so


%changelog
* Mon Sep 9 2024 Yichun Zhang (agentzh) 1.0.3-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.3.
* Mon Sep 2 2024 Yichun Zhang (agentzh) 1.0.2-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.2.
* Sat Aug 31 2024 Yichun Zhang (agentzh) 1.0.0-1
- init version of lua-resty-limit-traffic-dynamic.
