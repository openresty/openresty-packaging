Name:           openresty-plus-core-asan
Version:        1.19.9.1.56
Release:        1%{?dist}
Summary:        The AddressSanitizer (ASAN) version of OpenResty+

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        Proprietary
URL:            https://openresty.com/

Source0:        openresty-plus-%{version}.tar.gz
#Source1:        openresty-plus.init

%bcond_with	lua_ldap
%bcond_without	lua_resty_ldap
%bcond_without	lua_resty_openidc
%bcond_without	lua_resty_session
%bcond_without	lua_resty_openssl
%bcond_without	lua_resty_jwt
%bcond_without	lua_resty_hmac
%bcond_without	lua_resty_mlcache
%bcond_without	ngx_brotli
%bcond_without	lua_resty_mail
%bcond_with	tcmalloc

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl, systemtap-sdt-devel
BuildRequires:  openresty-zlib-asan-devel >= 1.2.11-17
BuildRequires:  openresty-plus-openssl111-asan-devel >= 1.1.1k-1
BuildRequires:  openresty-pcre-asan-devel >= 8.45-1
BuildRequires:  openresty-yajl-devel >= 2.1.0.4
BuildRequires:  libtool
BuildRequires:  gd-devel
BuildRequires:  glibc-devel
%if 0%{?coro_nginx_module}
BuildRequires:  openresty-libcco-devel
BuildRequires:  openresty-elf-loader-devel
BuildRequires:  openresty-cyrus-sasl-devel
BuildRequires:  openresty-libmariadb-devel
BuildRequires:  openresty-libmemcached-devel
BuildRequires:  openresty-hiredis-devel
BuildRequires:  openresty-elfutils-devel
%endif
%if %{with tcmalloc}
BuildRequires:  openresty-tcmalloc-devel
%endif

%if %{with lua_ldap}
%if 0%{?suse_version}
BuildRequires:  openldap2-devel
%else
BuildRequires:  openldap-devel
%endif
%endif
%ifarch x86_64
BuildRequires:  openresty-plus-hyperscan-devel >= 5.0.0-14
%endif
Requires:       openresty-zlib-asan >= 1.2.11-17
Requires:       openresty-plus-openssl111-asan >= 1.1.1k-i
Requires:       openresty-pcre-asan >= 8.45-1
Requires:       openresty-yajl >= 2.1.0.4
Requires:       openresty-maxminddb-asan >= 1.4.2.4-3
%if 0%{?coro_nginx_module}
Requires:       openresty-elfutils
Requires:       openresty-libcco
Requires:       openresty-elf-loader
%endif
%if %{with tcmalloc}
Requires:       openresty-tcmalloc
%endif

%if 0%{?suse_version} && 0%{?suse_version} >= 1500
Requires:       libgd3
%else
Requires:       gd
%endif

# needed by tcc
Requires:       glibc-devel
%if %{with lua_ldap}
%if 0%{?suse_version}
Requires:       openldap2
%else
Requires:       openldap
%endif
%endif

# for /sbin/service
#Requires(post):  chkconfig
#Requires(preun): chkconfig, initscripts

AutoReqProv:        no

%define orprefix            %{_usr}/local/openresty-plus-asan
%define zlib_prefix         %{_usr}/local/openresty-asan/zlib
%define pcre_prefix         %{_usr}/local/openresty-asan/pcre
%define openssl_prefix      %{_usr}/local/openresty-plus-asan/openssl111
%define maxminddb_prefix    %{_usr}/local/openresty-plus-asan/maxminddb
%define orutils_prefix      %{_usr}/local/openresty-utils
%define hyperscan_prefix    %{_usr}/local/openresty-plus/hyperscan
%define wasm_prefix         %{_usr}/local/openresty-plus/wasm

%define libcco_prefix       %{_usr}/local/libcco
%define elf_loader_prefix   %{_usr}/local/elf-loader
%define elfutils_prefix     %{_usr}/local/openresty-elfutils
%define tcmalloc_prefix     %{_usr}/local/openresty-tcmalloc
%define hiredis_prefix      %{_usr}/local/openresty-plus/hiredis
%define libmariadb_prefix   %{_usr}/local/openresty-plus/libmariadb
%define libmemcached_prefix %{_usr}/local/openresty-plus/libmemcached
%define cyrus_sasl_prefix   %{_usr}/local/openresty-plus/cyrus-sasl


%description
This package contains the gcc AddressSanitizer version of the core server
for OpenResty+ with gcc's AddressSanitizer built in.
Built for development & testing purposes only.

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


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openresty-plus-%{version}"; \
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


%package resty

Summary:        OpenResty+ command-line utility, resty
Group:          Development/Tools
Requires:       perl, openresty-plus-core >= %{version}-%{release}
Requires:       perl(File::Spec), perl(FindBin), perl(List::Util), perl(Getopt::Long), perl(File::Temp), perl(POSIX), perl(Time::HiRes)

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description resty
This package contains the "resty" command-line utility for OpenResty+, which
runs OpenResty Lua scripts on the terminal using a headless NGINX behind the
scene.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.


%package doc

Summary:        OpenResty+ documentation tool, restydoc
Group:          Development/Tools
Requires:       perl, perl(Getopt::Std), perl(File::Spec), perl(FindBin), perl(Cwd), perl(File::Temp), perl(Pod::Man), perl(Pod::Text)

%if (!0%{?rhel} || 0%{?rhel} < 7) && !0%{?fedora}
Requires:       groff
%endif

%if (0%{?rhel} && 0%{?rhel} >= 7) || 0%{?fedora}
Requires:       groff-base
%endif

Provides:       restydoc, restydoc-index, md2pod.pl

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description doc
This package contains the official OpenResty+ documentation index and
the "restydoc" command-line utility for viewing it.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.


%package opm

Summary:        OpenResty+ Package Manager
Group:          Development/Tools
Requires:       perl, openresty-plus-core >= %{version}-%{release}, perl(Digest::MD5)
Requires:       openresty-plus-core-doc >= %{version}-%{release}, openresty-plus-core-resty >= %{version}-%{release}
Requires:       curl, tar, gzip
#BuildRequires:  perl(Digest::MD5)
Requires:       perl(Encode), perl(FindBin), perl(File::Find), perl(File::Path), perl(File::Spec), perl(Cwd), perl(Digest::MD5), perl(File::Copy), perl(File::Temp), perl(Getopt::Long)

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description opm
This package provides the client side tool, opm, for OpenResty Pakcage Manager (OPM).


%package devel
Summary:            Development files for %{name}
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Development files for OpenResty+.


%prep
%setup -q -n "openresty-plus-%{version}"



%build

export ASAN_OPTIONS=detect_leaks=0
export ELF_LOADER_INC=%{elf_loader_prefix}/include
export ELF_LOADER_LIB=%{elf_loader_prefix}/lib
export CCO_INC=%{libcco_prefix}/include
export CCO_LIB=%{libcco_prefix}/lib

./configure \
    --prefix="%{orprefix}" \
    --with-lmdb-xcflags="-fPIC -O3 -g3 -DMDB_FDATASYNC_WORKS=1 -DMDB_BUILD_PRODUCT=plus-core" \
    --with-patlist-xcxxflags="-std=gnu++11 -g3 -Wall -Werror -O3" \
    --with-cc='ccache gcc -fdiagnostics-color=always -fsanitize=address -fno-omit-frame-pointer' \
    --with-cc-opt="-fPIC -DNGX_HTTP_LUA_CHECK_LICENSE -DNGX_LUA_ABORT_AT_PANIC -I%{zlib_prefix}/include -I%{pcre_prefix}/include \
%if 0%{?coro_nginx_module}
 -I%{elf_loader_prefix}/include -I%{libcco_prefix}/include -I%{hiredis_prefix}/include \
 -I%{libmariadb_prefix}/include/mariadb -I%{libmemcached_prefix}/include  \
 -I%{cyrus_sasl_prefix}/include/ \
%endif
%if %{with tcmalloc}
    -I%{tcmalloc_prefix}/include \
%endif
    -I%{openssl_prefix}/include -g" \
    --with-ld-opt="../license/en_plus_init.o -L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib \
%if 0%{?coro_nginx_module}
    -L%{elf_loader_prefix}/lib -L%{libcco_prefix}/lib -L%{elfutils_prefix}/lib \
    -Wl,-rpath,%{elfutils_prefix}/lib:%{elf_loader_prefix}/lib:%{libcco_prefix}/lib \
%endif
%if %{with tcmalloc}
    -L%{tcmalloc_prefix}/lib \
    -Wl,-rpath,%{tcmalloc_prefix}/lib \
    -ltcmalloc_minimal \
%endif
    -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
%ifarch x86_64
    --with-lua_resty_hyperscan \
%endif
    --with-pcre-jit \
%if %{with lua_ldap}
    --with-lua_ldap \
%endif
%if %{with lua_resty_ldap}
    --with-lua_resty_ldap \
%endif
%if %{with lua_resty_openidc}
    --with-lua_resty_openidc \
%endif
%if %{with lua_resty_session}
    --with-lua_resty_session \
%endif
%if %{with lua_resty_openssl}
    --with-lua_resty_openssl\
%endif
%if %{with lua_resty_jwt}
    --with-lua_resty_jwt \
%endif
%if %{with lua_resty_hmac}
    --with-lua_resty_hmac \
%endif
%if %{with lua_resty_mlcache}
    --with-lua_resty_mlcache \
%endif
%if %{with ngx_brotli}
    --with-ngx_brotli \
%endif
%if %{with lua_resty_mail}
    --with-lua_resty_mail \
%endif
%if 0%{?coro_nginx_module}
    --with-coro_nginx_module \
%endif
    --without-edge_message_bus \
    --without-edge_routing_platform \
    --without-edge_pki \
    --without-http_rds_json_module \
    --without-http_rds_csv_module \
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
    --without-lua_resty_upstream \
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
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-http_v2_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_gzip_static_module \
    --with-http_gunzip_module \
    --with-ngx_qat_module \
    --with-threads \
    --with-compat \
    --with-poll_module \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -g3 -DLUAJIT_ENABLE_GC64 -DLUAJIT_USE_SYSMALLOC' \
    --with-no-pool-patch \
    -j`nproc`

make -j`nproc` \
    CXX='ccache g++ -fsanitize=address'

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
make install-headers DESTDIR=%{buildroot}
ln -sf %{orutils_prefix}/bin/resty2 %{buildroot}%{orprefix}/bin/
ln -sf %{hyperscan_prefix}/lib/libhs.so %{buildroot}%{orprefix}/lualib/
ln -sf %{hyperscan_prefix}/lib/libhs_runtime.so %{buildroot}%{orprefix}/lualib/
ln -sf %{maxminddb_prefix}/lib/libmaxminddb.so %{buildroot}%{orprefix}/lualib/
ln -sf %{wasm_prefix}/lib/liborwasmrt.so %{buildroot}%{orprefix}/lualib/
%ifnarch x86_64
# NB: hyperscan.compiler is always required in edgelang, so put a fake lua module here.
install -d %{buildroot}%{orprefix}/lualib/resty/hyperscan/
echo 'return {}' > %{buildroot}%{orprefix}/lualib/resty/hyperscan/compiler.lua
%endif

pushd %{buildroot}

for f in `find .%{orprefix}/lualib -type f -name '*.lua'`; do
    LUA_PATH=".%{orprefix}/luajit/share/luajit-2.1/?.lua;;" .%{orprefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm -f $f
done

for f in `find .%{orprefix}/luajit -type f -name '*.lua'`; do
    LUA_PATH=".%{orprefix}/luajit/share/luajit-2.1/?.lua;.%{orprefix}/luajit/share/luajit-2.1/?.ljbc;;" .%{orprefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm -f $f
done

popd

rm -rf %{buildroot}%{orprefix}/luajit/share/man
rm -rf %{buildroot}%{orprefix}/luajit/lib/libluajit-5.1.a
rm -rf %{buildroot}%{orprefix}/lmdb/bin/mdb_{copy,load,stat,drop}
rm -rf %{buildroot}%{orprefix}/lmdb/lib/*.a
rm -rf %{buildroot}%{orprefix}/lmdb/include
rm -rf %{buildroot}%{orprefix}/lmdb/share
rm -rf %{buildroot}%{orprefix}/tcc/share


#mkdir -p %{buildroot}/etc/init.d

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%{orprefix}/COPYRIGHT
%{orprefix}/bin/openresty-plus
%{orprefix}/bin/resty2
%{orprefix}/site/lualib/
%{orprefix}/luajit/*
%{orprefix}/lualib/*
%{orprefix}/lmdb/bin/mdb_dump
%{orprefix}/lmdb/lib/liblmdb.so
%{orprefix}/nginx/html/*
%{orprefix}/nginx/logs/
%{orprefix}/nginx/sbin/*
%{orprefix}/nginx/modules/*
%{orprefix}/tcc/bin/tcc
%{orprefix}/tcc/lib/*
%{orprefix}/tcc/include/*
%config(noreplace) %{orprefix}/nginx/conf/*


%files resty
%defattr(-,root,root,-)

%{orprefix}/bin/resty


%files doc
%defattr(-,root,root,-)

%{orprefix}/bin/md2pod.pl
%{orprefix}/bin/nginx-xml2pod


%files opm
%defattr(-,root,root,-)

%{orprefix}/bin/opm
%{orprefix}/site/manifest/
%{orprefix}/site/pod/


%files devel
%{orprefix}/build


%changelog
* Thu Mar 21 2024 Yichun Zhang (agentzh) 1.19.9.1.56-1
- upgraded openresty-plus to 1.19.9.1.56.
* Tue Mar 19 2024 Yichun Zhang (agentzh) 1.19.9.1.55-1
- upgraded openresty-plus to 1.19.9.1.55.
* Wed Mar 13 2024 Yichun Zhang (agentzh) 1.19.9.1.54-1
- upgraded openresty-plus to 1.19.9.1.54.
* Wed Feb 28 2024 Yichun Zhang (agentzh) 1.19.9.1.53-1
- upgraded openresty-plus to 1.19.9.1.53.
* Wed Jan 3 2024 Yichun Zhang (agentzh) 1.19.9.1.52-1
- upgraded openresty-plus to 1.19.9.1.52.
* Wed Nov 29 2023 Yichun Zhang (agentzh) 1.19.9.1.51-1
- upgraded openresty-plus to 1.19.9.1.51.
* Wed Oct 25 2023 Yichun Zhang (agentzh) 1.19.9.1.50-1
- upgraded openresty-plus to 1.19.9.1.50.
* Thu Sep 7 2023 Yichun Zhang (agentzh) 1.19.9.1.49-1
- upgraded openresty-plus to 1.19.9.1.49.
* Tue Sep 5 2023 Yichun Zhang (agentzh) 1.19.9.1.48-1
- upgraded openresty-plus to 1.19.9.1.48.
* Thu Aug 24 2023 Yichun Zhang (agentzh) 1.19.9.1.47-1
- upgraded openresty-plus to 1.19.9.1.47.
* Mon Aug 14 2023 Yichun Zhang (agentzh) 1.19.9.1.46-1
- upgraded openresty-plus to 1.19.9.1.46.
* Thu Aug 3 2023 Yichun Zhang (agentzh) 1.19.9.1.45-1
- upgraded openresty-plus to 1.19.9.1.45.
* Tue Aug 1 2023 Yichun Zhang (agentzh) 1.19.9.1.44-1
- upgraded openresty-plus to 1.19.9.1.44.
* Mon Jul 24 2023 Yichun Zhang (agentzh) 1.19.9.1.43-1
- upgraded openresty-plus to 1.19.9.1.43.
* Tue Jul 18 2023 Yichun Zhang (agentzh) 1.19.9.1.42-1
- upgraded openresty-plus to 1.19.9.1.42.
* Tue Jul 4 2023 Yichun Zhang (agentzh) 1.19.9.1.40-1
- upgraded openresty-plus to 1.19.9.1.40.
* Thu May 25 2023 Yichun Zhang (agentzh) 1.19.9.1.39-1
- upgraded openresty-plus to 1.19.9.1.39.
* Fri Apr 14 2023 Yichun Zhang (agentzh) 1.19.9.1.38-1
- upgraded openresty-plus to 1.19.9.1.38.
* Mon Apr 10 2023 Yichun Zhang (agentzh) 1.19.9.1.37-1
- upgraded openresty-plus to 1.19.9.1.37.
* Mon Apr 3 2023 Yichun Zhang (agentzh) 1.19.9.1.36-1
- upgraded openresty-plus to 1.19.9.1.36.
* Mon Mar 20 2023 Yichun Zhang (agentzh) 1.19.9.1.35-1
- upgraded openresty-plus to 1.19.9.1.35.
* Mon Mar 6 2023 Yichun Zhang (agentzh) 1.19.9.1.34-1
- upgraded openresty-plus to 1.19.9.1.34.
* Fri Feb 24 2023 Yichun Zhang (agentzh) 1.19.9.1.33-1
- upgraded openresty-plus to 1.19.9.1.33.
* Thu Feb 9 2023 Yichun Zhang (agentzh) 1.19.9.1.32-1
- upgraded openresty-plus to 1.19.9.1.32.
* Mon Jan 16 2023 Yichun Zhang (agentzh) 1.19.9.1.31-1
- upgraded openresty-plus to 1.19.9.1.31.
* Wed Jan 11 2023 Yichun Zhang (agentzh) 1.19.9.1.30-1
- upgraded openresty-plus to 1.19.9.1.30.
* Tue Jan 3 2023 Yichun Zhang (agentzh) 1.19.9.1.29-1
- upgraded openresty-plus to 1.19.9.1.29.
* Mon Jan 2 2023 Yichun Zhang (agentzh) 1.19.9.1.28-1
- upgraded openresty-plus to 1.19.9.1.28.
* Mon Jan 2 2023 Yichun Zhang (agentzh) 1.19.9.1.27-1
- upgraded openresty-plus to 1.19.9.1.27.
* Mon Dec 26 2022 Yichun Zhang (agentzh) 1.19.9.1.26-1
- upgraded openresty-plus to 1.19.9.1.26.
* Thu Dec 8 2022 Yichun Zhang (agentzh) 1.19.9.1.25-1
- upgraded openresty-plus to 1.19.9.1.25.
* Mon Nov 28 2022 Yichun Zhang (agentzh) 1.19.9.1.24-1
- upgraded openresty-plus to 1.19.9.1.24.
* Thu Nov 24 2022 Yichun Zhang (agentzh) 1.19.9.1.23-1
- upgraded openresty-plus to 1.19.9.1.23.
* Tue Nov 22 2022 Yichun Zhang (agentzh) 1.19.9.1.22-1
- upgraded openresty-plus to 1.19.9.1.22.
* Thu Oct 27 2022 Yichun Zhang (agentzh) 1.19.9.1.21-1
- upgraded openresty-plus to 1.19.9.1.21.
* Tue Oct 25 2022 Yichun Zhang (agentzh) 1.19.9.1.20-1
- upgraded openresty-plus to 1.19.9.1.20.
* Wed Oct 19 2022 Yichun Zhang (agentzh) 1.19.9.1.19-1
- upgraded openresty-plus to 1.19.9.1.19.
* Fri Sep 16 2022 Yichun Zhang (agentzh) 1.19.9.1.18-1
- upgraded openresty-plus to 1.19.9.1.18.
* Fri Jul 15 2022 Yichun Zhang (agentzh) 1.19.9.1.17-1
- upgraded openresty-plus to 1.19.9.1.17.
* Wed Jun 1 2022 Yichun Zhang (agentzh) 1.19.9.1.16-1
- upgraded openresty-plus to 1.19.9.1.16.
* Wed Apr 20 2022 Yichun Zhang (agentzh) 1.19.9.1.15-1
- upgraded openresty-plus to 1.19.9.1.15.
* Wed Apr 13 2022 Yichun Zhang (agentzh) 1.19.9.1.14-1
- upgraded openresty-plus to 1.19.9.1.14.
* Thu Apr 7 2022 Yichun Zhang (agentzh) 1.19.9.1.13-1
- upgraded openresty-plus to 1.19.9.1.13.
* Tue Mar 29 2022 Yichun Zhang (agentzh) 1.19.9.1.12-1
- upgraded openresty-plus to 1.19.9.1.12.
* Wed Mar 16 2022 Yichun Zhang (agentzh) 1.19.9.1.11-1
- upgraded openresty-plus to 1.19.9.1.11.
* Tue Mar 8 2022 Yichun Zhang (agentzh) 1.19.9.1.10-1
- upgraded openresty-plus to 1.19.9.1.10.
* Sun Mar 6 2022 Yichun Zhang (agentzh) 1.19.9.1.9-1
- upgraded openresty-plus to 1.19.9.1.9.
* Mon Jan 3 2022 Yichun Zhang (agentzh) 1.19.9.1.8-1
- upgraded openresty-plus to 1.19.9.1.8.
* Mon Dec 13 2021 Yichun Zhang (agentzh) 1.19.9.1.7-1
- upgraded openresty-plus to 1.19.9.1.7.
* Tue Dec 7 2021 Yichun Zhang (agentzh) 1.19.9.1.6-1
- upgraded openresty-plus to 1.19.9.1.6.
* Wed Nov 17 2021 Wang Hui (wanghuizzz) 1.19.9.1.5-1
- initial packaging.
