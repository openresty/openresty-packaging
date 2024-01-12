Name:           lua-resty-redis-cluster-fast-1.21.4
Version:        0.0.4
Release:        1%{?dist}
Summary:        Redis cluster client for OpenResty

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/
BuildArch:      noarch

Source0:        lua-resty-redis-cluster-fast-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# LuaJIT is required to compile Lua files into bytecode
BuildRequires:  openresty >= 1.17.8.2

Requires:  coro-hiredis-nginx-module-1.21.4 >= 0.0.5-1

AutoReqProv:        no

%define orprefix                        %{_usr}/local/openresty
%define lua_lib_dir                     %{orprefix}/site/lualib


%description
This is a client that supports the redis cluster for OpenResty.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-resty-redis-cluster-fast-%{version}"; \
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
%setup -q -n "lua-resty-redis-cluster-fast-%{version}"


%build
make
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
for f in `find lib/resty/ -type f -name '*.lua'`; do
    %{orprefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm $f
done


%install
rm -rf %{buildroot}
sed -i 's|lib/resty/redis/cluster/fast/\*.lua|lib/resty/redis/cluster/fast/\*.ljbc|g' Makefile
sed -i 's|lib/resty/redis/cluster/fast/cmd/\*.lua|lib/resty/redis/cluster/fast/cmd/\*.ljbc|g' Makefile
sed -i 's|lib/resty/redis/cluster/fast.lua|lib/resty/redis/cluster/fast.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{lua_lib_dir}/resty/redis/cluster/
%dir %{lua_lib_dir}/resty/redis/cluster/fast
%dir %{lua_lib_dir}/resty/redis/cluster/fast/cmd
%{lua_lib_dir}/resty/redis/cluster/*


%changelog
* Wed Apr 5 2023 Yichun Zhang (agentzh) 0.0.3-1
- upgraded lua-resty-redis-cluster-fast to 0.0.3.
* Tue Apr 4 2023 Yichun Zhang (agentzh) 0.0.2-1
- upgraded lua-resty-redis-cluster-fast to 0.0.2.
* Sat Mar 25 2023 Hui Wang 0.0.1-1
- initial build for lua-resty-redis-cluster-fast.
