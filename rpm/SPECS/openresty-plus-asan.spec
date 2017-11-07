Name:           openresty-plus-asan
Version:        1.13.6.0.4
Release:        2%{?dist}
Summary:        The clang AddressSanitizer version of OpenResty+

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        Proprietary
URL:            https://www.openresty.com/

Source0:        openresty-plus-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc, make, perl, valgrind-devel, clang

BuildRequires:  perl-File-Temp
BuildRequires:  openresty-zlib-asan-devel >= 1.2.11-6
BuildRequires:  openresty-openssl-asan-devel >= 1.0.2k-2
BuildRequires:  openresty-pcre-asan-devel >= 8.41-1
BuildRequires:  gd-devel
Requires:       openresty-zlib-asan >= 1.2.11-6
Requires:       openresty-openssl-asan >= 1.0.2k-2
Requires:       openresty-pcre-asan >= 8.41-1
Requires:       gd

AutoReqProv:        no

%define orprefix            %{_usr}/local/%{name}
%define openssl_prefix      %{_usr}/local/openresty-asan/openssl
%define zlib_prefix         %{_usr}/local/openresty-asan/zlib
%define pcre_prefix         %{_usr}/local/openresty-asan/pcre

%if 0%{?el6}
%undefine _missing_build_ids_terminate_build
%endif

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openresty-plus-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
%{nil}


%description
This package contains the clang AddressSanitizer version of the core server
for OpenResty+ for Valgrind. Built for development & testing purposes only.

DO NOT USE THIS PACKAGE IN PRODUCTION!

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

By taking advantage of various well-designed Nginx modules (most of which
are developed by the OpenResty team themselves), OpenResty effectively
turns the nginx server into a powerful web app server, in which the web
developers can use the Lua programming language to script various existing
nginx C modules and Lua modules and construct extremely high-performance
web applications that are capable to handle 10K ~ 1000K+ connections in
a single box.


%prep
%setup -q -n "openresty-plus-%{version}"


%build
export ASAN_OPTIONS=detect_leaks=0

./configure \
    --prefix="%{orprefix}" \
    --with-debug \
    --with-cc="clang -fsanitize=address" \
    --with-cc-opt="-DNGX_LUA_ABORT_AT_PANIC -DNGX_LUA_USE_ASSERT -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -O1" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
    --with-pcre-jit \
    --without-http_rds_json_module \
    --without-http_rds_csv_module \
    --without-lua_rds_parser \
    --without-http_xss_module \
    --without-http_form_input_module \
    --without-http_srcache_module \
    --without-http_lua_upstream_module \
    --without-http_array_var_module \
    --without-http_memc_module \
    --without-http_redis2_module \
    --without-http_redis_module \
    --without-lua_redis_parser \
    --without-lua_rds_parser \
    --without-lua_resty_upstream_healthcheck \
    --without-select_module \
    --without-http_userid_module \
    --without-http_autoindex_module \
    --without-http_geo_module \
    --without-http_split_clients_module \
    --without-http_fastcgi_module \
    --without-http_uwsgi_module \
    --without-http_scgi_module \
    --without-http_memcached_module \
    --without-http_limit_conn_module \
    --without-http_limit_req_module \
    --without-http_empty_gif_module \
    --without-http_browser_module \
    --without-http_upstream_hash_module \
    --without-http_upstream_ip_hash_module \
    --without-http_upstream_least_conn_module \
    --without-http_upstream_zone_module \
    --without-mail_pop3_module \
    --without-mail_imap_module \
    --without-mail_smtp_module \
    --without-stream_limit_conn_module \
    --without-stream_return_module \
    --without-stream_upstream_hash_module \
    --without-stream_upstream_least_conn_module \
    --without-stream_upstream_zone_module \
    --with-stream \
    --with-stream_ssl_module \
    --with-http_v2_module \
    --without-mail_pop3_module \
    --without-mail_imap_module \
    --without-mail_smtp_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_gzip_static_module \
    --with-http_gunzip_module \
    --with-threads \
    --with-file-aio \
    --with-poll_module \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -DLUAJIT_USE_VALGRIND -O1 -fno-omit-frame-pointer' \
    --with-no-pool-patch \
    %{?_smp_mflags} 1>&2

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

pushd %{buildroot}

for f in `find .%{orprefix}/lualib -type f -name '*.lua'`; do
    LUA_PATH=".%{orprefix}/luajit/share/luajit-2.1.0-beta3/?.lua;;" .%{orprefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm -f $f
done

popd

rm -rf %{buildroot}%{orprefix}/luajit/share/man
rm -rf %{buildroot}%{orprefix}/luajit/lib/libluajit-5.1.a
rm -rf %{buildroot}%{orprefix}/bin/resty
rm -rf %{buildroot}%{orprefix}/bin/restydoc
rm -rf %{buildroot}%{orprefix}/bin/restydoc-index
rm -rf %{buildroot}%{orprefix}/bin/md2pod.pl
rm -rf %{buildroot}%{orprefix}/bin/opm
rm -rf %{buildroot}%{orprefix}/bin/nginx-xml2pod
rm -rf %{buildroot}%{orprefix}/pod/*
rm -rf %{buildroot}%{orprefix}/resty.index

mkdir -p %{buildroot}/usr/bin
ln -sf %{orprefix}/nginx/sbin/nginx %{buildroot}/usr/bin/%{name}

# to suppress the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

/usr/bin/%{name}
%{orprefix}/COPYRIGHT
%{orprefix}/bin/openresty-plus
%{orprefix}/site/lualib/
%{orprefix}/luajit/*
%{orprefix}/lualib/*
%{orprefix}/nginx/html/*
%{orprefix}/nginx/logs/
%{orprefix}/nginx/sbin/*
%config(noreplace) %{orprefix}/nginx/conf/*


%changelog
* Tue Nov 7 2017 Yichun Zhang (agentzh) 1.13.6.0.4-2
- required openresty-pcre* 8.41-1.
* Thu Nov 2 2017 Yichun Zhang (agentzh) 1.13.6.0.4-1
- upgraded openresty-plus to 1.13.6.0.4.
* Thu Sep 21 2017 Yichun Zhang (agentzh) 1.11.2.5-2
- enabled -DNGX_LUA_ABORT_AT_PANIC and -DNGX_LUA_USE_ASSERT by default.
* Thu Aug 31 2017 Yichun Zhang 1.11.2.5.1-1
- upgraded openresty plus to 1.11.2.5.1.
* Sat Jul 29 2017 Yichun Zhang 1.11.2.4.4-1
- upgraded openresty plus to 1.11.2.4.4.
* Sat Jul 15 2017 Yichun Zhang 1.11.2.4.3-1
- upgraded openresty plus to 1.11.2.4.3.
* Sat Jul 15 2017 Yichun Zhang 1.11.2.4.2-1
- fixed spec for CentOS 6 regarding missing build id issues.
* Sat Jul 15 2017 Yichun Zhang 1.11.2.4.2-1
- initial build for OpenResty+ 1.11.2.4.2.
