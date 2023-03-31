Name:           openresty-coro-hiredis-nginx-module
Version:        0.0.2
Release:        1%{?dist}
Summary:        Coroutine implemented hiredis nginx module for OpenResty

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

%define or_version           1.21.4.2rc1

Source0:        coro-hiredis-nginx-module-%{version}.tar.gz
Source1:        openresty-%{or_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl
BuildRequires:  openresty-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-pcre-devel
BuildRequires:  openresty-elf-loader-devel
BuildRequires:  openresty-libcco-devel
BuildRequires:  openresty-elfutils-devel
BuildRequires:  openresty-coro-nginx-module-devel
BuildRequires:  openresty-hiredis-devel
BuildRequires:  openresty
Requires:       openresty-coro-nginx-module, openresty-hiredis

AutoReqProv:        no

%define prefix             /usr/local/openresty-coro-nginx-module
%define or_prefix          /usr/local/openresty
%define zlib_prefix        %{or_prefix}/zlib
%define pcre_prefix        %{or_prefix}/pcre
%define openssl_prefix     %{or_prefix}/openssl111
%define lua_lib_dir        %{or_prefix}/site/lualib
%define elf_loader_prefix  /usr/local/elf-loader
%define elfutils_prefix    /usr/local/openresty-elfutils
%define hiredis_prefix     /usr/local/openresty-plus/hiredis


%description
This is the coroutine implemented hiredis nginx module for OpenResty.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/coro-hiredis-nginx-module-%{version}"; \
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
%setup -q -n "coro-hiredis-nginx-module-%{version}"
tar xzf %{SOURCE1}


%build
cd openresty-*
./configure \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-DNGX_HTTP_CORO_USE_FREE_LISTS -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -I%{elfutils_prefix}/include -I%{elf_loader_prefix}/include -I%{prefix}/include -I%{hiredis_prefix}/include" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -L%{elfutils_prefix}/lib -L%{elf_loader_prefix}/lib -L%{prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib:%{elfutils_prefix}/lib:%{elf_loader_prefix}/lib:%{prefix}/lib" \
    --with-compat \
    --add-dynamic-module=../ \
    -j`nproc`

make -C build/nginx-*/ modules -j`nproc`

cd ..
for f in `find lualib/resty/ -type f -name '*.lua'`; do
    %{or_prefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm $f
done


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{prefix}/lib
mkdir -p %{buildroot}%{lua_lib_dir}/resty
cd openresty-*
install -m755 build/nginx-*/objs/*.so %{buildroot}%{prefix}/lib/
cd ..
sed -i 's|lib/resty/\*.lua|lib/resty/\*.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}


# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{prefix}/lib/ngx_http_coro_hiredis_module.so
%{lua_lib_dir}/resty/hiredis.ljbc


%changelog
* Thu Mar 30 2023 Yichun Zhang (agentzh) 0.0.2-1
- upgraded openresty-coro-hiredis-nginx-module to 0.0.2.
* Thu Mar 30 2023 Hui Wang 0.0.1-1
- initial build for openresty-coro-hiredis-nginx-module.
