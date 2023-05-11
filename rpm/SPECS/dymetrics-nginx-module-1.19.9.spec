Name:           dymetrics-nginx-module-1.19.9
Version:        0.0.15
Release:        1%{?dist}
Summary:        dymetrics nginx module for OpenResty

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

%define ngx_version          1.19.9
%define or_version           1.19.9.1

Source0:        lua-resty-dymetrics-%{version}.tar.gz
Source1:        https://openresty.org/download/openresty-%{or_version}.tar.gz

Patch0:         nginx-%{ngx_version}-proc_exit_handler.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl
BuildRequires:  openresty-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-pcre-devel

AutoReqProv:        no

%define or_prefix          /usr/local/openresty
%define zlib_prefix        %{or_prefix}/zlib
%define pcre_prefix        %{or_prefix}/pcre
%define openssl_prefix     %{or_prefix}/openssl111
%define lua_lib_dir        %{or_prefix}/site/lualib


%description
This is the dymetrics nginx module for OpenResty.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-resty-dymetrics-%{version}"; \
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
%setup -q -n "lua-resty-dymetrics-%{version}"
tar xzf %{SOURCE1}

cd openresty-%{or_version}/bundle/nginx-%{ngx_version}
%patch0 -p1


%build
cd openresty-*
./configure \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-I%{zlib_prefix}/include -I%{pcre_prefix}/include -O3" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
    --with-pcre-jit \
    --without-http_rds_json_module \
    --without-http_rds_csv_module \
    --without-lua_rds_parser \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-http_v2_module \
    --without-mail_pop3_module \
    --without-mail_imap_module \
    --without-mail_smtp_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_secure_link_module \
    --with-http_random_index_module \
    --with-http_gzip_static_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-threads \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT' \
    --with-compat \
    --with-compat \
    --add-dynamic-module=../ \
    -j`nproc`

make -C build/nginx-*/ modules -j`nproc`

%install
rm -rf %{buildroot}
cd openresty-*
mkdir -p %{buildroot}%{or_prefix}/nginx/lib
install -m755 build/nginx-*/objs/*.so %{buildroot}%{or_prefix}/nginx/lib/


# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{or_prefix}/nginx/lib/ngx_http_lua_dymetrics_module.so


%changelog
* Thu May 11 2023 Yichun Zhang (agentzh) 0.0.15-1
- upgraded dymetrics-nginx-module to 0.0.15.
