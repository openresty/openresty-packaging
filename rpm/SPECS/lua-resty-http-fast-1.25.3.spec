Name:           lua-resty-http-fast-1.25.3
Version:        0.0.7
Release:        1%{?dist}
Summary:        http client library using coro

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/
BuildArch:      noarch

Source0:        lua-resty-http-fast-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# LuaJIT is required to compile Lua files into bytecode
BuildRequires:  openresty >= 1.17.8.2

Requires:  coro-libcurl-nginx-module-1.25.3 >= 0.0.1-1

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
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-resty-http-fast-%{version}"; \
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
%setup -q -n "lua-resty-http-fast-%{version}"


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
sed -i 's|lib/resty/http/fast/\*.lua|lib/resty/http/fast/\*.ljbc|g' Makefile
sed -i 's|lib/resty/http/\*.lua|lib/resty/http/\*.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %{lua_lib_dir}/resty/http/fast/
%{lua_lib_dir}/resty/http/*.ljbc
%{lua_lib_dir}/resty/http/fast/*.ljbc


%changelog
* Mon Oct 14 2024 Yichun Zhang (agentzh) 0.0.7-1
- upgraded lua-resty-http-fast to 0.0.7.
* Thu Oct 10 2024 Yichun Zhang (agentzh) 0.0.6-1
- upgraded lua-resty-http-fast to 0.0.6.
* Mon Oct 7 2024 Yichun Zhang (agentzh) 0.0.4-1
- upgraded lua-resty-http-fast to 0.0.4.
* Sun Oct 6 2024 Yichun Zhang (agentzh) 0.0.2-1
- upgraded lua-resty-http-fast to 0.0.2.
* Sat Mar 25 2023 Hui Wang 0.0.1-1
- initial build for lua-resty-http-fast.
