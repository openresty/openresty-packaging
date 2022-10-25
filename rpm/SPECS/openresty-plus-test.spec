Name:           openresty-plus-test
Version:        1.19.9.1.20
Release:        1%{?dist}
Summary:        OpenResty+, enhanced version of scalable web platform by extending NGINX with Lua

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

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl, systemtap-sdt-devel
BuildRequires:  openresty-zlib-devel >= 1.2.11-3
BuildRequires:  openresty-plus-openssl111-devel >= 1.1.1k-1
BuildRequires:  openresty-pcre-devel >= 8.44-1
BuildRequires:  openresty-yajl-devel >= 2.1.0.4
BuildRequires:  libtool
BuildRequires:  gd-devel
BuildRequires:  glibc-devel
%if %{with lua_ldap}
%if 0%{?suse_version}
BuildRequires:  openldap2-devel
%else
BuildRequires:  openldap-devel
%endif
%endif
%ifarch x86_64
BuildRequires:  openresty-plus-hyperscan-devel
Requires:       openresty-plus-hyperscan
%endif
Requires:       openresty-zlib >= 1.2.11-3
Requires:       openresty-plus-openssl111 >= 1.1.1k-1
Requires:       openresty-pcre >= 8.44-1
Requires:       openresty-yajl >= 2.1.0.4
Requires:       openresty-maxminddb >= 1.4.2.4

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

%define orprefix            %{_usr}/local/%{name}
%define zlib_prefix         %{_usr}/local/openresty/zlib
%define pcre_prefix         %{_usr}/local/openresty/pcre
%define openssl_prefix      %{_usr}/local/openresty-plus/openssl111
%define orutils_prefix      %{_usr}/local/openresty-utils
%define hyperscan_prefix    %{_usr}/local/openresty-plus/hyperscan
%define maxminddb_prefix    %{_usr}/local/openresty-plus/maxminddb

%define lj_debug_cc_opts    -DLUAJIT_SECURITY_STRID=0 -DLUAJIT_SECURITY_STRHASH=0 -DLUAJIT_SECURITY_PRNG=0 -DLUAJIT_SECURITY_MCODE=0 -DLUA_USE_APICHECK -DLUA_USE_ASSERT

%description
This package contains the debug version of the core server for OpenResty+.
Built for running test purposes only.

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
Requires:       perl, openresty-plus-test >= %{version}-%{release}
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
Requires:       perl, openresty-plus-test >= %{version}-%{release}, perl(Digest::MD5)
Requires:       curl, tar, gzip
#BuildRequires:  perl(Digest::MD5)
Requires:       perl(Encode), perl(FindBin), perl(File::Find), perl(File::Path), perl(File::Spec), perl(Cwd), perl(Digest::MD5), perl(File::Copy), perl(File::Temp), perl(Getopt::Long)

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description opm
This package provides the client side tool, opm, for OpenResty Pakcage Manager (OPM).


%prep
%setup -q -n "openresty-plus-%{version}"


%build
./configure \
    --prefix="%{orprefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-DNGX_LUA_ABORT_AT_PANIC -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -g3" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
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
    --with-lua_resty_openssl \
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
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-http_v2_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_gzip_static_module \
    --with-http_gunzip_module \
    --with-ngx_qat_module \
    --with-threads \
    --with-compat  \
    --with-luajit-xcflags='%{lj_debug_cc_opts} -DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -g3 -DLUAJIT_ENABLE_GC64' \
    -j`nproc`

make -j`nproc`

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
ln -sf %{orutils_prefix}/bin/resty2 %{buildroot}%{orprefix}/bin/
ln -sf %{hyperscan_prefix}/lib/libhs.so %{buildroot}%{orprefix}/lualib/
ln -sf %{hyperscan_prefix}/lib/libhs_runtime.so %{buildroot}%{orprefix}/lualib/
ln -sf %{maxminddb_prefix}/lib/libmaxminddb.so %{buildroot}%{orprefix}/lualib/
%ifnarch x86_64
# NB: hyperscan.compiler is always required in edgelang, so put a fake lua module here.
install -d %{buildroot}%{orprefix}/lualib/resty/hyperscan/
echo 'return {}' > %{buildroot}%{orprefix}/lualib/resty/hyperscan/compiler.lua
%endif

pushd %{buildroot}

for f in `find .%{orprefix}/lualib -type f -name '*.lua'`; do
    LUA_PATH=".%{orprefix}/luajit/share/luajit-2.1.0-beta3/?.lua;;" .%{orprefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
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


%changelog
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
* Mon Nov 15 2021 Yichun Zhang (agentzh) 1.19.9.1.5-1
- upgraded openresty-plus to 1.19.9.1.5.
* Sun Nov 7 2021 Yichun Zhang (agentzh) 1.19.9.1.4-1
- upgraded openresty-plus to 1.19.9.1.4.
* Thu Nov 4 2021 Yichun Zhang (agentzh) 1.19.9.1.3-1
- upgraded openresty-plus to 1.19.9.1.3.
* Thu Sep 23 2021 Yichun Zhang (agentzh) 1.19.9.1.2-1
- upgraded openresty-plus to 1.19.9.1.2.
* Fri Sep 17 2021 Yichun Zhang (agentzh) 1.19.9.1.1-1
- upgraded openresty-plus to 1.19.9.1.1.
* Tue Aug 24 2021 Yichun Zhang (agentzh) 1.19.3.1.40-1
- upgraded openresty-plus to 1.19.3.1.40.
* Tue Aug 24 2021 Yichun Zhang (agentzh) 1.19.3.1.39-1
- upgraded openresty-plus to 1.19.3.1.39.
* Tue Aug 17 2021 Yichun Zhang (agentzh) 1.19.3.1.38-1
- upgraded openresty-plus to 1.19.3.1.38.
* Mon Jul 26 2021 Yichun Zhang (agentzh) 1.19.3.1.37-1
- upgraded openresty-plus to 1.19.3.1.37.
* Wed Jun 23 2021 Yichun Zhang (agentzh) 1.19.3.1.36-1
- upgraded openresty-plus to 1.19.3.1.36.
* Sun Jun 20 2021 Yichun Zhang (agentzh) 1.19.3.1.35-1
- upgraded openresty-plus to 1.19.3.1.35.
* Mon Jun 7 2021 Yichun Zhang (agentzh) 1.19.3.1.34-1
- upgraded openresty-plus to 1.19.3.1.34.
* Tue May 25 2021 Yichun Zhang (agentzh) 1.19.3.1.33-1
- upgraded openresty-plus to 1.19.3.1.33.
* Mon May 24 2021 Yichun Zhang (agentzh) 1.19.3.1.32-1
- upgraded openresty-plus to 1.19.3.1.32.
* Wed May 19 2021 Yichun Zhang (agentzh) 1.19.3.1.31-1
- upgraded openresty-plus to 1.19.3.1.31.
* Tue May 11 2021 Yichun Zhang (agentzh) 1.19.3.1.30-1
- upgraded openresty-plus to 1.19.3.1.30.
* Thu Apr 29 2021 Yichun Zhang (agentzh) 1.19.3.1.29-1
- upgraded openresty-plus to 1.19.3.1.29.
* Wed Apr 28 2021 Yichun Zhang (agentzh) 1.19.3.1.28-1
- upgraded openresty-plus to 1.19.3.1.28.
* Thu Apr 22 2021 Yichun Zhang (agentzh) 1.19.3.1.27-1
- upgraded openresty-plus to 1.19.3.1.27.
* Mon Apr 19 2021 Yichun Zhang (agentzh) 1.19.3.1.26-1
- upgraded openresty-plus to 1.19.3.1.26.
* Wed Apr 14 2021 Yichun Zhang (agentzh) 1.19.3.1.25-1
- upgraded openresty-plus to 1.19.3.1.25.
* Fri Apr 9 2021 Yichun Zhang (agentzh) 1.19.3.1.24-1
- upgraded openresty-plus to 1.19.3.1.24.
* Tue Apr 6 2021 Yichun Zhang (agentzh) 1.19.3.1.22-1
- upgraded openresty-plus to 1.19.3.1.22.
* Wed Mar 31 2021 Yichun Zhang (agentzh) 1.19.3.1.21-1
- upgraded openresty-plus to 1.19.3.1.21.
* Sat Mar 27 2021 Yichun Zhang (agentzh) 1.19.3.1.20-1
- upgraded openresty-plus to 1.19.3.1.20.
* Thu Mar 25 2021 Yichun Zhang (agentzh) 1.19.3.1.19-1
- upgraded openresty-plus to 1.19.3.1.19.
* Sat Mar 20 2021 Yichun Zhang (agentzh) 1.19.3.1.18-1
- upgraded openresty-plus to 1.19.3.1.18.
* Fri Mar 12 2021 Yichun Zhang (agentzh) 1.19.3.1.17-1
- upgraded openresty-plus to 1.19.3.1.17.
* Wed Mar 10 2021 Yichun Zhang (agentzh) 1.19.3.1.16-1
- upgraded openresty-plus to 1.19.3.1.16.
* Tue Mar 9 2021 Yichun Zhang (agentzh) 1.19.3.1.15-1
- upgraded openresty-plus to 1.19.3.1.15.
* Mon Mar 08 2021 Wang Jiahao (wangjiahao) 1.19.3.1.14-1
- initial packaging.
