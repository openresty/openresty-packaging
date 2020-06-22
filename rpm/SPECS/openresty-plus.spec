Name:           openresty-plus
Version:        1.15.8.2.10
Release:        1%{?dist}
Summary:        OpenResty+, enhanced version of scalable web platform by extending NGINX with Lua

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        Proprietary
URL:            https://openresty.com/

Source0:        openresty-plus-%{version}.tar.gz
#Source1:        openresty-plus.init

%bcond_without	lua_ldap

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl
BuildRequires:  openresty-zlib-devel >= 1.2.11-3
BuildRequires:  openresty-openssl-devel >= 1.1.0j
BuildRequires:  openresty-pcre-devel >= 8.41-1
BuildRequires:  gd-devel
BuildRequires:  glibc-devel, texinfo
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
Requires:       openresty-openssl >= 1.1.0j
Requires:       openresty-pcre >= 8.41-1
Requires:       gd
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
%define openssl_prefix      %{_usr}/local/openresty/openssl

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{name}-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%description
This package contains the core server for OpenResty+, an enhanced version of
OpenResty. Built for production uses.

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


%package resty

Summary:        OpenResty+ command-line utility, resty
Group:          Development/Tools
Requires:       perl, openresty-plus >= %{version}-%{release}
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
Requires:       perl, openresty-plus >= %{version}-%{release}, perl(Digest::MD5)
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
    --with-threads \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -g3 -DLUAJIT_ENABLE_GC64' \
    %{?_smp_mflags}

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
%{orprefix}/site/lualib/
%{orprefix}/luajit/*
%{orprefix}/lualib/*
%{orprefix}/lmdb/bin/mdb_dump
%{orprefix}/lmdb/lib/liblmdb.so
%{orprefix}/nginx/html/*
%{orprefix}/nginx/logs/
%{orprefix}/nginx/sbin/*
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
* Tue Oct 31 2017 Yichun Zhang (agentzh) 1.13.6.0.3-1
- upgraded openresty-plus to 1.13.6.0.3.
* Mon Oct 30 2017 Yichun Zhang (agentzh) 1.13.6.0.2-1
- upgraded openresty-plus to 1.13.6.0.2.
* Fri Oct 27 2017 Yichun Zhang (agentzh) 1.13.6.0.1-2
- upgraded openresty-plus to 1.13.6.0.1.
* Fri Oct 27 2017 Yichun Zhang (agentzh) 1.13.6.0.1-1
- upgraded openresty-plus to 1.13.6.0.1.
* Thu Oct 26 2017 Yichun Zhang (agentzh) 1.13.5.0.2-1
- upgraded openresty-plus to 1.13.5.0.2.
* Wed Oct 25 2017 Yichun Zhang (agentzh) 1.13.5.0.1-1
- upgraded openresty-plus to 1.13.5.0.1.
* Tue Oct 17 2017 Yichun Zhang (agentzh) 1.11.2.5.11-1
- upgraded openresty-plus to 1.11.2.5.11.
* Mon Oct 16 2017 Yichun Zhang (agentzh) 1.11.2.5.10-1
- upgraded openresty-plus to 1.11.2.5.10.
* Wed Oct 4 2017 Yichun Zhang (agentzh) 1.11.2.5.9-1
- upgraded openresty-plus to 1.11.2.5.9.
* Fri Sep 29 2017 Yichun Zhang (agentzh) 1.11.2.5.8-1
- upgraded openresty-plus to 1.11.2.5.8.
* Fri Sep 29 2017 Yichun Zhang (agentzh) 1.11.2.5.7-1
- upgraded openresty-plus to 1.11.2.5.7.
* Wed Sep 27 2017 Yichun Zhang (agentzh) 1.11.2.5.6-1
- upgraded openresty-plus to 1.11.2.5.6.
* Tue Sep 26 2017 Yichun Zhang (agentzh) 1.11.2.5.5-1
- upgraded openresty-plus to 1.11.2.5.5.
* Mon Sep 25 2017 Yichun Zhang (agentzh) 1.11.2.5.4-1
- upgraded openresty-plus to 1.11.2.5.4.
* Fri Sep 22 2017 Yichun Zhang (agentzh) 1.11.2.5.3-1
- upgraded openresty-plus to 1.11.2.5.3.
* Thu Sep 21 2017 Yichun Zhang (agentzh) 1.11.2.5.2-1
- upgraded openresty-plus to 1.11.2.5.2.
* Thu Sep 21 2017 Yichun Zhang (agentzh) 1.11.2.5.1-2
- enabled -DNGX_LUA_ABORT_AT_PANIC by default.
* Thu Aug 31 2017 Yichun Zhang 1.11.2.5.1-1
- upgraded openresty plus to 1.11.2.5.1.
* Mon Aug 14 2017 Yichun Zhang 1.11.2.4.8-1
- upgraded openresty plus to 1.11.2.4.8.
* Sun Aug 13 2017 Yichun Zhang 1.11.2.4.7-1
- upgraded openresty plus to 1.11.2.4.7.
* Mon Aug 7 2017 Yichun Zhang 1.11.2.4.6-2
- removed the useless init script reg & dereg commands.
* Sun Aug 6 2017 Yichun Zhang 1.11.2.4.6-1
- upgraded openresty plus to 1.11.2.4.6.
* Fri Aug 4 2017 Yichun Zhang 1.11.2.4.5-1
- upgraded openresty plus to 1.11.2.4.5.
* Sat Jul 29 2017 Yichun Zhang 1.11.2.4.4-1
- upgraded openresty plus to 1.11.2.4.4.
* Sat Jul 15 2017 Yichun Zhang 1.11.2.4.3-1
- upgraded openresty plus to 1.11.2.4.3.
* Thu Jul 13 2017 Yichun Zhang 1.11.2.4.2-2
- removed systemtap dtrace USDT probes to avoid any risk of GPL pollutions.
* Wed Jul 12 2017 Yichun Zhang 1.11.2.4.2-1
- upgraded to 1.11.2.4.2.
* Wed Jul 12 2017 Yichun Zhang 1.11.2.4.1-1
- upgraded to 1.11.2.4.1.
* Mon Jul 3 2017 Yichun Zhang 1.11.2.3.13-1
- upgraded to 1.11.2.3.13.
* Sun Jul 2 2017 Yichun Zhang 1.11.2.3.12-1
- upgraded to 1.11.2.3.12.
* Sat Jul 1 2017 Yichun Zhang 1.11.2.3.11-1
- upgraded to 1.11.2.3.11.
* Fri Jun 30 2017 Yichun Zhang 1.11.2.3.10-1
- upgraded to 1.11.2.3.10.
* Mon Jun 26 2017 Yichun Zhang 1.11.2.3.9-1
- upgraded to 1.11.2.3.9.
- replaced lualib/*.lua with lualib/*.ljbc.
* Mon Jun 26 2017 Yichun Zhang 1.11.2.3.8-2
- excluded source code from the debuginfo package.
* Mon Jun 26 2017 Yichun Zhang 1.11.2.3.8-1
- upgraded to 1.11.2.3.8.
* Mon Jun 26 2017 Yichun Zhang 1.11.2.3.7-2
- removed components we do not need.
* Sat Jun 24 2017 Yichun Zhang 1.11.2.3.7-1
- upgraded to 1.11.2.3.7.
* Sat Jun 17 2017 Yichun Zhang 1.11.2.3.6-1
- upgraded to 1.11.2.3.6.
* Wed Jun 14 2017 Yichun Zhang 1.11.2.3.5-1
- upgraded to 1.11.2.3.5.
* Mon Jun 12 2017 Yichun Zhang 1.11.2.3.4-1
- upgraded to 1.11.2.3.4.
* Fri Jun 9 2017 Yichun Zhang 1.11.2.3.3-1
- upgraded to 1.11.2.3.3.
* Thu Jun 1 2017 Yichun Zhang 1.11.2.3.2-1
- bugfix: installed the Lua modules shipped with ngx_lua_ssl_module.
* Tue May 30 2017 Yichun Zhang 1.11.2.3.1-4
- temporarily bundled the GeoLite2 database for internal use.
* Tue May 30 2017 Yichun Zhang 1.11.2.3.1-3
- removed the init script.
* Sun May 28 2017 Yichun Zhang (agentzh) 1.11.2.3.1-2
- fixed the init script.
* Sun May 28 2017 Yichun Zhang (agentzh) 1.11.2.3.1-1
- initial packaging.
