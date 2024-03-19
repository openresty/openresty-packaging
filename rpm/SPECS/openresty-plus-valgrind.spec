Name:           openresty-plus-valgrind
Version:        1.19.9.1.55
Release:        1%{?dist}
Summary:        The Valgrind debug version of OpenResty+

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        Proprietary
URL:            https://www.openresty.com/

Source0:        openresty-plus-%{version}.tar.gz

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

BuildRequires:  ccache, gcc, make, perl, valgrind-devel
Requires:       valgrind

BuildRequires:  perl-File-Temp
BuildRequires:  openresty-zlib-devel >= 1.2.11-3
BuildRequires:  openresty-plus-openssl111-debug-devel >= 1.1.1k-1
BuildRequires:  openresty-pcre-devel >= 8.45-1
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
%endif
Requires:       openresty-zlib >= 1.2.11-3
Requires:       openresty-plus-openssl111-debug >= 1.1.1k-1
Requires:       openresty-pcre >= 8.45-1
Requires:       openresty-maxminddb >= 1.4.2.3
# needed by tcc
Requires:       glibc-devel

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

AutoReqProv:        no

%define orprefix            %{_usr}/local/%{name}
%define openssl_prefix      %{_usr}/local/openresty-plus-debug/openssl111
%define zlib_prefix         %{_usr}/local/openresty/zlib
%define pcre_prefix         %{_usr}/local/openresty/pcre
%define orutils_prefix      %{_usr}/local/openresty-utils
%define hyperscan_prefix    %{_usr}/local/openresty-plus/hyperscan
%define maxminddb_prefix    %{_usr}/local/openresty-plus/maxminddb

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openresty-plus-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%description
This package contains a debug version of the core server for OpenResty+ for Valgrind.
Built for development purposes only.

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
./configure \
    --prefix="%{orprefix}" \
    --with-debug \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-DNGX_LUA_ABORT_AT_PANIC -DNGX_LUA_USE_ASSERT -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -O0 -g3" \
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
    --with-stream_ssl_preread_module \
    --with-http_v2_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_gzip_static_module \
    --with-ngx_qat_module \
    --with-http_gunzip_module \
    --with-threads \
    --with-compat  \
    --with-poll_module \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -DLUAJIT_USE_VALGRIND -DLUAJIT_USE_SYSMALLOC -O0 -g3 -DLUAJIT_ENABLE_GC64' \
    --with-no-pool-patch \
    -j`nproc` 1>&2

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
    LUA_PATH=".%{orprefix}/luajit/share/luajit-2.1/?.lua;;" .%{orprefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm -f $f
done

popd

rm -rf %{buildroot}%{orprefix}/luajit/share/man
rm -rf %{buildroot}%{orprefix}/luajit/lib/libluajit-5.1.a
rm -rf %{buildroot}%{orprefix}/bin/resty
rm -rf %{buildroot}%{orprefix}/bin/md2pod.pl
rm -rf %{buildroot}%{orprefix}/bin/opm
rm -rf %{buildroot}%{orprefix}/bin/nginx-xml2pod
rm -rf %{buildroot}%{orprefix}/pod/*
rm -rf %{buildroot}%{orprefix}/resty.index
rm -rf %{buildroot}%{orprefix}/lmdb/bin/mdb_{copy,load,stat,drop}
rm -rf %{buildroot}%{orprefix}/lmdb/lib/*.a
rm -rf %{buildroot}%{orprefix}/lmdb/include
rm -rf %{buildroot}%{orprefix}/lmdb/share
rm -rf %{buildroot}%{orprefix}/tcc/share

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


%changelog
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
* Fri Mar 5 2021 Yichun Zhang (agentzh) 1.19.3.1.14-1
- upgraded openresty-plus to 1.19.3.1.14.
* Fri Mar 5 2021 Yichun Zhang (agentzh) 1.19.3.1.13-1
- upgraded openresty-plus to 1.19.3.1.13.
* Mon Mar 1 2021 Yichun Zhang (agentzh) 1.19.3.1.12-1
- upgraded openresty-plus to 1.19.3.1.12.
* Fri Feb 26 2021 Yichun Zhang (agentzh) 1.19.3.1.11-1
- upgraded openresty-plus to 1.19.3.1.11.
* Tue Feb 9 2021 Yichun Zhang (agentzh) 1.19.3.1.9-1
- upgraded openresty-plus to 1.19.3.1.9.
* Wed Feb 3 2021 Yichun Zhang (agentzh) 1.19.3.1.8-1
- upgraded openresty-plus to 1.19.3.1.8.
* Fri Jan 15 2021 Yichun Zhang (agentzh) 1.19.3.1.7-1
- upgraded openresty-plus to 1.19.3.1.7.
* Tue Dec 29 2020 Yichun Zhang (agentzh) 1.19.3.1.6-1
- upgraded openresty-plus to 1.19.3.1.6.
* Thu Dec 24 2020 Yichun Zhang (agentzh) 1.19.3.1.5-1
- upgraded openresty-plus to 1.19.3.1.5.
* Thu Dec 24 2020 Yichun Zhang (agentzh) 1.19.3.1.4-1
- upgraded openresty-plus to 1.19.3.1.4.
* Tue Nov 17 2020 Yichun Zhang (agentzh) 1.19.3.1.3-1
- upgraded openresty-plus to 1.19.3.1.3.
* Fri Nov 13 2020 Yichun Zhang (agentzh) 1.19.3.1.1-1
- upgraded openresty-plus to 1.19.3.1.1.
* Tue Oct 27 2020 Yichun Zhang (agentzh) 1.17.8.2.10-1
- upgraded openresty-plus to 1.17.8.2.10.
* Tue Oct 27 2020 Yichun Zhang (agentzh) 1.17.8.2.9-1
- upgraded openresty-plus to 1.17.8.2.9.
* Tue Oct 13 2020 Yichun Zhang (agentzh) 1.17.8.2.8-1
- upgraded openresty-plus to 1.17.8.2.8.
* Fri Oct 9 2020 Yichun Zhang (agentzh) 1.17.8.2.7-1
- upgraded openresty-plus to 1.17.8.2.7.
* Thu Oct 1 2020 Yichun Zhang (agentzh) 1.17.8.2.6-1
- upgraded openresty-plus to 1.17.8.2.6.
* Thu Oct 1 2020 Yichun Zhang (agentzh) 1.17.8.2.5-1
- upgraded openresty-plus to 1.17.8.2.5.
* Wed Sep 30 2020 Yichun Zhang (agentzh) 1.17.8.2.4-1
- upgraded openresty-plus to 1.17.8.2.4.
* Wed Sep 02 2020 Johnny Wang (johnny) 1.17.8.2.3-1
- upgraded openresty-plus to 1.17.8.2.3.
* Thu Aug 27 2020 Yichun Zhang (agentzh) 1.17.8.2.2-1
- upgraded openresty-plus to 1.17.8.2.2.
* Wed Aug 26 2020 Yichun Zhang (agentzh) 1.17.8.2.1-1
- upgraded openresty-plus to 1.17.8.2.1.
* Thu Aug 20 2020 Yichun Zhang (agentzh) 1.17.8.2.0-1
- upgraded openresty-plus to 1.17.8.2.0.
* Sun Jun 21 2020 Yichun Zhang (agentzh) 1.15.8.2.10-1
- upgraded openresty-plus to 1.15.8.2.10.
* Sat Jun 6 2020 Yichun Zhang (agentzh) 1.15.8.2.9-1
- upgraded openresty-plus to 1.15.8.2.9.
* Sat Apr 4 2020 Yichun Zhang (agentzh) 1.15.8.2.8-1
- upgraded openresty-plus to 1.15.8.2.8.
* Sun Mar 22 2020 Yichun Zhang (agentzh) 1.15.8.2.7-1
- upgraded openresty-plus to 1.15.8.2.7.
* Mon Mar 9 2020 Yichun Zhang (agentzh) 1.15.8.2.6-1
- upgraded openresty-plus to 1.15.8.2.6.
* Wed Jan 29 2020 Yichun Zhang (agentzh) 1.15.8.2.5-1
- upgraded openresty-plus to 1.15.8.2.5.
* Thu Jan 2 2020 Yichun Zhang (agentzh) 1.15.8.2.4-1
- upgraded openresty-plus to 1.15.8.2.4.
* Fri Sep 20 2019 Yichun Zhang (agentzh) 1.15.8.2.3-1
- upgraded openresty-plus to 1.15.8.2.3.
* Tue Sep 17 2019 Yichun Zhang (agentzh) 1.15.8.2.2-1
- upgraded openresty-plus to 1.15.8.2.2.
* Wed Sep 11 2019 Yichun Zhang (agentzh) 1.15.8.2.1-1
- upgraded openresty-plus to 1.15.8.2.1.
* Thu Aug 8 2019 Yichun Zhang (agentzh) 1.15.8.1.12-1
- upgraded openresty-plus to 1.15.8.1.12.
* Thu Aug 1 2019 Yichun Zhang (agentzh) 1.15.8.1.11-1
- upgraded openresty-plus to 1.15.8.1.11.
* Thu Aug 1 2019 Yichun Zhang (agentzh) 1.15.8.1.10-1
- upgraded openresty-plus to 1.15.8.1.10.
* Mon Jul 29 2019 Yichun Zhang (agentzh) 1.15.8.1.9-1
- upgraded openresty-plus to 1.15.8.1.9.
* Thu Jul 11 2019 Yichun Zhang (agentzh) 1.15.8.1.8-1
- upgraded openresty-plus to 1.15.8.1.8.
* Mon Jul 1 2019 Yichun Zhang (agentzh) 1.15.8.1.7-1
- upgraded openresty-plus to 1.15.8.1.7.
* Wed Jun 26 2019 Yichun Zhang (agentzh) 1.15.8.1.6-1
- upgraded openresty-plus to 1.15.8.1.6.
* Wed Jun 19 2019 Yichun Zhang (agentzh) 1.15.8.1.5-1
- upgraded openresty-plus to 1.15.8.1.5.
* Mon Jun 17 2019 Yichun Zhang (agentzh) 1.15.8.1.4-1
- upgraded openresty-plus to 1.15.8.1.4.
* Thu Jun 6 2019 Yichun Zhang (agentzh) 1.15.8.1.3-1
- upgraded openresty-plus to 1.15.8.1.3.
* Thu May 30 2019 Yichun Zhang (agentzh) 1.15.8.1.2-1
- upgraded openresty-plus to 1.15.8.1.2.
* Tue May 28 2019 Yichun Zhang (agentzh) 1.15.8.1.1-1
- upgraded openresty-plus to 1.15.8.1.1.
* Mon May 27 2019 Yichun Zhang (agentzh) 1.15.8.1.0-1
- upgraded openresty-plus to 1.15.8.1.0.
* Fri May 17 2019 Yichun Zhang (agentzh) 1.13.6.2.64-1
- upgraded openresty-plus to 1.13.6.2.64.
* Wed May 15 2019 Yichun Zhang (agentzh) 1.13.6.2.63-1
- upgraded openresty-plus to 1.13.6.2.63.
* Tue Apr 30 2019 Yichun Zhang (agentzh) 1.13.6.2.62-1
- upgraded openresty-plus to 1.13.6.2.62.
* Fri Apr 26 2019 Yichun Zhang (agentzh) 1.13.6.2.61-1
- upgraded openresty-plus to 1.13.6.2.61.
* Wed Apr 24 2019 Yichun Zhang (agentzh) 1.13.6.2.60-1
- upgraded openresty-plus to 1.13.6.2.60.
* Mon Apr 1 2019 Yichun Zhang (agentzh) 1.13.6.2.59-1
- upgraded openresty-plus to 1.13.6.2.59.
* Sat Mar 30 2019 Yichun Zhang (agentzh) 1.13.6.2.58-1
- upgraded openresty-plus to 1.13.6.2.58.
* Wed Mar 27 2019 Yichun Zhang (agentzh) 1.13.6.2.57-1
- upgraded openresty-plus to 1.13.6.2.57.
* Wed Mar 20 2019 Yichun Zhang (agentzh) 1.13.6.2.56-1
- upgraded openresty-plus to 1.13.6.2.56.
* Fri Mar 1 2019 Yichun Zhang (agentzh) 1.13.6.2.55-1
- upgraded openresty-plus to 1.13.6.2.55.
* Sun Feb 10 2019 Yichun Zhang (agentzh) 1.13.6.2.53-1
- upgraded openresty-plus to 1.13.6.2.53.
* Wed Jan 30 2019 Yichun Zhang (agentzh) 1.13.6.2.52-1
- upgraded openresty-plus to 1.13.6.2.52.
* Sun Jan 20 2019 Yichun Zhang (agentzh) 1.13.6.2.51-1
- upgraded openresty-plus to 1.13.6.2.51.
* Wed Jan 16 2019 Yichun Zhang (agentzh) 1.13.6.2.50-1
- upgraded openresty-plus to 1.13.6.2.50.
* Mon Jan 7 2019 Yichun Zhang (agentzh) 1.13.6.2.49-1
- upgraded openresty-plus to 1.13.6.2.49.
* Fri Jan 4 2019 Yichun Zhang (agentzh) 1.13.6.2.48-1
- upgraded openresty-plus to 1.13.6.2.48.
* Thu Jan 3 2019 Yichun Zhang (agentzh) 1.13.6.2.47-1
- upgraded openresty-plus to 1.13.6.2.47.
* Tue Jan 1 2019 Yichun Zhang (agentzh) 1.13.6.2.46-1
- upgraded openresty-plus to 1.13.6.2.46.
* Mon Dec 31 2018 Yichun Zhang (agentzh) 1.13.6.2.45-1
- upgraded openresty-plus to 1.13.6.2.45.
* Sun Dec 30 2018 Yichun Zhang (agentzh) 1.13.6.2.44-1
- upgraded openresty-plus to 1.13.6.2.44.
* Sun Dec 30 2018 Yichun Zhang (agentzh) 1.13.6.2.43-1
- upgraded openresty-plus to 1.13.6.2.43.
* Thu Dec 27 2018 Yichun Zhang (agentzh) 1.13.6.2.42-1
- upgraded openresty-plus to 1.13.6.2.42.
* Mon Dec 24 2018 Yichun Zhang (agentzh) 1.13.6.2.41-1
- upgraded openresty-plus to 1.13.6.2.41.
* Wed Dec 19 2018 Yichun Zhang (agentzh) 1.13.6.2.40-1
- upgraded openresty-plus to 1.13.6.2.40.
* Mon Dec 17 2018 Yichun Zhang (agentzh) 1.13.6.2.39-1
- upgraded openresty-plus to 1.13.6.2.39.
* Sat Dec 15 2018 Yichun Zhang (agentzh) 1.13.6.2.38-1
- upgraded openresty-plus to 1.13.6.2.38.
* Sat Dec 15 2018 Yichun Zhang (agentzh) 1.13.6.2.37-1
- upgraded openresty-plus to 1.13.6.2.37.
* Sat Dec 15 2018 Yichun Zhang (agentzh) 1.13.6.2.36-1
- upgraded openresty-plus to 1.13.6.2.36.
* Sat Dec 15 2018 Yichun Zhang (agentzh) 1.13.6.2.35-1
- upgraded openresty-plus to 1.13.6.2.35.
* Fri Dec 14 2018 Yichun Zhang (agentzh) 1.13.6.2.34-1
- upgraded openresty-plus to 1.13.6.2.34.
* Tue Dec 11 2018 Yichun Zhang (agentzh) 1.13.6.2.33-1
- upgraded openresty-plus to 1.13.6.2.33.
* Mon Dec 10 2018 Yichun Zhang (agentzh) 1.13.6.2.32-1
- upgraded openresty-plus to 1.13.6.2.32.
* Sun Dec 9 2018 Yichun Zhang (agentzh) 1.13.6.2.31-1
- upgraded openresty-plus to 1.13.6.2.31.
* Sun Dec 2 2018 Yichun Zhang (agentzh) 1.13.6.2.30-1
- upgraded openresty-plus to 1.13.6.2.30.
* Thu Nov 22 2018 Yichun Zhang (agentzh) 1.13.6.2.29-1
- upgraded openresty-plus to 1.13.6.2.29.
* Thu Nov 15 2018 Yichun Zhang (agentzh) 1.13.6.2.28-1
- upgraded openresty-plus to 1.13.6.2.28.
* Mon Nov 5 2018 Yichun Zhang (agentzh) 1.13.6.2.27-1
- upgraded openresty-plus to 1.13.6.2.27.
* Sat Oct 6 2018 Yichun Zhang (agentzh) 1.13.6.2.26-1
- upgraded openresty-plus to 1.13.6.2.26.
* Mon Sep 17 2018 Yichun Zhang (agentzh) 1.13.6.2.25-1
- upgraded openresty-plus to 1.13.6.2.25.
* Wed Sep 5 2018 Yichun Zhang (agentzh) 1.13.6.2.24-1
- upgraded openresty-plus to 1.13.6.2.24.
* Mon Sep 3 2018 Yichun Zhang (agentzh) 1.13.6.2.23-1
- upgraded openresty-plus to 1.13.6.2.23.
* Tue Aug 21 2018 Yichun Zhang (agentzh) 1.13.6.2.22-1
- upgraded openresty-plus to 1.13.6.2.22.
* Wed Aug 8 2018 Yichun Zhang (agentzh) 1.13.6.2.21-1
- upgraded openresty-plus to 1.13.6.2.21.
* Tue Aug 7 2018 Yichun Zhang (agentzh) 1.13.6.2.20-1
- upgraded openresty-plus to 1.13.6.2.20.
* Mon Jul 16 2018 Yichun Zhang (agentzh) 1.13.6.2.19-1
- upgraded openresty-plus to 1.13.6.2.19.
* Tue Jul 10 2018 Yichun Zhang (agentzh) 1.13.6.2.18-1
- upgraded openresty-plus to 1.13.6.2.18.
* Mon Jul 2 2018 Yichun Zhang (agentzh) 1.13.6.2.17-1
- upgraded openresty-plus to 1.13.6.2.17.
* Sun Jul 1 2018 Yichun Zhang (agentzh) 1.13.6.2.16-1
- upgraded openresty-plus to 1.13.6.2.16.
* Sat Jun 30 2018 Yichun Zhang (agentzh) 1.13.6.2.15-1
- upgraded openresty-plus to 1.13.6.2.15.
* Sun Jun 24 2018 Yichun Zhang (agentzh) 1.13.6.2.14-1
- upgraded openresty-plus to 1.13.6.2.14.
* Sat Jun 23 2018 Yichun Zhang (agentzh) 1.13.6.2.13-1
- upgraded openresty-plus to 1.13.6.2.13.
* Wed Jun 20 2018 Yichun Zhang (agentzh) 1.13.6.2.12-1
- upgraded openresty-plus to 1.13.6.2.12.
* Wed Jun 20 2018 Yichun Zhang (agentzh) 1.13.6.2.11-1
- upgraded openresty-plus to 1.13.6.2.11.
* Thu Jun 14 2018 Yichun Zhang (agentzh) 1.13.6.2.10-1
- upgraded openresty-plus to 1.13.6.2.10.
* Wed Jun 13 2018 Yichun Zhang (agentzh) 1.13.6.2.9-1
- upgraded openresty-plus to 1.13.6.2.9.
* Mon Jun 11 2018 Yichun Zhang (agentzh) 1.13.6.2.8-1
- upgraded openresty-plus to 1.13.6.2.8.
* Wed Jun 6 2018 Yichun Zhang (agentzh) 1.13.6.2.7-1
- upgraded openresty-plus to 1.13.6.2.7.
* Mon Jun 4 2018 Yichun Zhang (agentzh) 1.13.6.2.6-1
- upgraded openresty-plus to 1.13.6.2.6.
* Wed May 30 2018 Yichun Zhang (agentzh) 1.13.6.2.5-1
- upgraded openresty-plus to 1.13.6.2.5.
* Thu May 24 2018 Yichun Zhang (agentzh) 1.13.6.2.3-1
- upgraded openresty-plus to 1.13.6.2.3.
* Thu May 24 2018 Yichun Zhang (agentzh) 1.13.6.2.2-1
- upgraded openresty-plus to 1.13.6.2.2.
* Tue May 22 2018 Yichun Zhang (agentzh) 1.13.6.2.1-1
- upgraded openresty-plus to 1.13.6.2.1.
* Thu May 3 2018 Yichun Zhang (agentzh) 1.13.6.1.33-1
- upgraded openresty-plus to 1.13.6.1.33.
* Mon Apr 23 2018 Yichun Zhang (agentzh) 1.13.6.1.32-1
- upgraded openresty-plus to 1.13.6.1.32.
* Fri Apr 20 2018 Yichun Zhang (agentzh) 1.13.6.1.30-1
- upgraded openresty-plus to 1.13.6.1.30.
* Sat Apr 14 2018 Yichun Zhang (agentzh) 1.13.6.1.29-1
- upgraded openresty-plus to 1.13.6.1.29.
* Fri Apr 6 2018 Yichun Zhang (agentzh) 1.13.6.1.28-1
- upgraded openresty-plus to 1.13.6.1.28.
* Fri Apr 6 2018 Yichun Zhang (agentzh) 1.13.6.1.27-1
- upgraded openresty-plus to 1.13.6.1.27.
* Thu Apr 5 2018 Yichun Zhang (agentzh) 1.13.6.1.26-1
- upgraded openresty-plus to 1.13.6.1.26.
* Fri Mar 30 2018 Yichun Zhang (agentzh) 1.13.6.1.25-1
- upgraded openresty-plus to 1.13.6.1.25.
* Fri Mar 30 2018 Yichun Zhang (agentzh) 1.13.6.1.24-1
- upgraded openresty-plus to 1.13.6.1.24.
* Tue Mar 27 2018 Yichun Zhang (agentzh) 1.13.6.1.23-1
- upgraded openresty-plus to 1.13.6.1.23.
* Sun Mar 18 2018 Yichun Zhang (agentzh) 1.13.6.1.22-1
- upgraded openresty-plus to 1.13.6.1.22.
* Sun Mar 18 2018 Yichun Zhang (agentzh) 1.13.6.1.21-1
- upgraded openresty-plus to 1.13.6.1.21.
* Sat Mar 17 2018 Yichun Zhang (agentzh) 1.13.6.1.20-1
- upgraded openresty-plus to 1.13.6.1.20.
* Thu Mar 8 2018 Yichun Zhang (agentzh) 1.13.6.1.19-1
- upgraded openresty-plus to 1.13.6.1.19.
* Wed Mar 7 2018 Yichun Zhang (agentzh) 1.13.6.1.18-1
- upgraded openresty-plus to 1.13.6.1.18.
* Mon Feb 5 2018 Yichun Zhang (agentzh) 1.13.6.1.17-1
- upgraded openresty-plus to 1.13.6.1.17.
* Fri Jan 19 2018 Yichun Zhang (agentzh) 1.13.6.1.16-1
- upgraded openresty-plus to 1.13.6.1.16.
* Sun Jan 14 2018 Yichun Zhang (agentzh) 1.13.6.1.15-1
- upgraded openresty-plus to 1.13.6.1.15.
* Thu Jan 4 2018 Yichun Zhang (agentzh) 1.13.6.1.14-1
- upgraded openresty-plus to 1.13.6.1.14.
* Thu Dec 28 2017 Yichun Zhang (agentzh) 1.13.6.1.13-1
- upgraded openresty-plus to 1.13.6.1.13.
* Sun Dec 24 2017 Yichun Zhang (agentzh) 1.13.6.1.12-1
- upgraded openresty-plus to 1.13.6.1.12.
* Fri Dec 22 2017 Yichun Zhang (agentzh) 1.13.6.1.11-1
- upgraded openresty-plus to 1.13.6.1.11.
* Sun Dec 17 2017 Yichun Zhang (agentzh) 1.13.6.1.10-1
- upgraded openresty-plus to 1.13.6.1.10.
* Sun Dec 17 2017 Yichun Zhang (agentzh) 1.13.6.1.9-1
- upgraded openresty-plus to 1.13.6.1.9.
* Sat Dec 16 2017 Yichun Zhang (agentzh) 1.13.6.1.8-1
- upgraded openresty-plus to 1.13.6.1.8.
* Thu Dec 7 2017 Yichun Zhang (agentzh) 1.13.6.1.7-1
- upgraded openresty-plus to 1.13.6.1.7.
* Wed Dec 6 2017 Yichun Zhang (agentzh) 1.13.6.1.6-1
- upgraded openresty-plus to 1.13.6.1.6.
* Wed Dec 6 2017 Yichun Zhang (agentzh) 1.13.6.1.5-1
- upgraded openresty-plus to 1.13.6.1.5.
* Sun Nov 26 2017 Yichun Zhang (agentzh) 1.13.6.1.4-1
- upgraded openresty-plus to 1.13.6.1.4.
* Fri Nov 17 2017 Yichun Zhang (agentzh) 1.13.6.1.3-1
- upgraded openresty-plus to 1.13.6.1.3.
* Wed Nov 15 2017 Yichun Zhang (agentzh) 1.13.6.1.2-1
- upgraded openresty-plus to 1.13.6.1.2.
* Mon Nov 13 2017 Yichun Zhang (agentzh) 1.13.6.1.1-1
- upgraded openresty-plus to 1.13.6.1.1.
* Sun Nov 12 2017 Yichun Zhang (agentzh) 1.13.6.0.8-1
- upgraded openresty-plus to 1.13.6.0.8.
* Sat Nov 11 2017 Yichun Zhang (agentzh) 1.13.6.0.6-1
- upgraded openresty-plus to 1.13.6.0.6.
* Thu Nov 9 2017 Yichun Zhang (agentzh) 1.13.6.0.5-1
- upgraded openresty-plus to 1.13.6.0.5.
* Tue Nov 7 2017 Yichun Zhang (agentzh) 1.13.6.0.4-2
- required openresty-pcre* 8.41-1.
* Thu Nov 2 2017 Yichun Zhang (agentzh) 1.13.6.0.4-1
- upgraded openresty-plus to 1.13.6.0.4.
* Thu Sep 21 2017 Yichun Zhang (agentzh) 1.11.2.5.1-2
- enabled -DNGX_LUA_ABORT_AT_PANIC and -DNGX_LUA_USE_ASSERT by default.
* Thu Aug 31 2017 Yichun Zhang 1.11.2.5.1-1
- upgraded openresty plus to 1.11.2.5.1.
* Sat Jul 29 2017 Yichun Zhang 1.11.2.4.4-1
- upgraded openresty plus to 1.11.2.4.4.
* Sat Jul 15 2017 Yichun Zhang 1.11.2.4.3-1
- upgraded openresty plus to 1.11.2.4.3.
* Wed Jul 12 2017 Yichun Zhang 1.11.2.4.2-1
- upgraded to 1.11.2.4.2.
* Wed Jul 12 2017 Yichun Zhang 1.11.2.4.1-1
- upgraded to 1.11.2.4.1.
* Mon Jul 3 2017 Yichun Zhang 1.11.2.3.13-1
- upgraded to 1.11.2.3.13.
* Thu Jun 1 2017 Yichun Zhang 1.11.2.3.2-1
- bugfix: installed the Lua modules shipped with ngx_lua_ssl_module.
* Sun May 28 2017 Yichun Zhang (agentzh) 1.11.2.3.1-1
- initial packaging.
