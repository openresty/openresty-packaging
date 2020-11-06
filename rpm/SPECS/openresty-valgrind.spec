Name:           openresty-valgrind
Version:        1.19.3.1
Release:        1%{?dist}
Summary:        The Valgrind debug version of OpenResty

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            https://openresty.org/


Source0:        https://openresty.org/download/openresty-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc, make, perl, valgrind-devel, systemtap-sdt-devel
Requires:       valgrind

BuildRequires:  ccache, perl-File-Temp
BuildRequires:  openresty-zlib-devel >= 1.2.11-3
BuildRequires:  openresty-openssl111-debug-devel >= 1.1.1h-1
BuildRequires:  openresty-pcre-devel >= 8.44-1
Requires:       openresty-zlib >= 1.2.11-3
Requires:       openresty-openssl111-debug >= 1.1.1h-1
Requires:       openresty-pcre >= 8.44-1

AutoReqProv:        no

%define orprefix            %{_usr}/local/%{name}
%define openssl_prefix      %{_usr}/local/openresty-debug/openssl111
%define zlib_prefix         %{_usr}/local/openresty/zlib
%define pcre_prefix         %{_usr}/local/openresty/pcre

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openresty-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%if 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%description
This package contains a debug version of the core server for OpenResty for Valgrind.
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
%setup -q -n "openresty-%{version}"


%build
./configure \
    --prefix="%{orprefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-debug \
    --with-cc-opt="-I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -O0" \
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
    --with-poll_module \
    --with-compat \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -DLUAJIT_USE_VALGRIND -DLUAJIT_USE_SYSMALLOC -O0' \
    --with-no-pool-patch \
    %{?_smp_mflags}

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

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
%{orprefix}/bin/openresty
%{orprefix}/site/lualib/
%{orprefix}/luajit/*
%{orprefix}/lualib/*
%{orprefix}/nginx/html/*
%{orprefix}/nginx/logs/
%{orprefix}/nginx/sbin/*
%config(noreplace) %{orprefix}/nginx/conf/*
%{orprefix}/COPYRIGHT


%changelog
* Fri Nov 6 2020 Yichun Zhang (agentzh) 1.19.3.1-1
- upgraded openresty to 1.19.3.1.
* Mon Jul 13 2020 Yichun Zhang (agentzh) 1.17.8.2-1
- upgraded openresty to 1.17.8.2.
* Fri Jul 3 2020 Yichun Zhang (agentzh) 1.17.8.1-1
- upgraded openresty to 1.17.8.1.
* Thu Aug 29 2019 Yichun Zhang (agentzh) 1.15.8.2-1
- upgraded openresty to 1.15.8.2.
* Thu May 16 2019 Yichun Zhang (agentzh) 1.15.8.1-1
- upgraded openresty to 1.15.8.1.
* Mon May 14 2018 Yichun Zhang (agentzh) 1.13.6.2-1
- upgraded openresty to 1.13.6.2.
* Sun Nov 12 2017 Yichun Zhang (agentzh) 1.13.6.1-1
- upgraded openresty to 1.13.6.1.
* Thu Sep 21 2017 Yichun Zhang (agentzh) 1.11.2.5-2
- enabled -DNGX_LUA_ABORT_AT_PANIC and -DNGX_LUA_USE_ASSERT by default.
* Thu Aug 17 2017 Yichun Zhang (agentzh) 1.11.2.5-1
- upgraded OpenResty to 1.11.2.5.
* Tue Jul 11 2017 Yichun Zhang (agentzh) 1.11.2.4-1
- upgraded OpenResty to 1.11.2.4.
* Sun May 21 2017 Yichun Zhang (agentzh) 1.11.2.3-3
- removed the geoip nginx module since GeoIP is not available everywhere.
* Fri Apr 21 2017 Yichun Zhang (agentzh)
- upgrade to the OpenResty 1.11.2.3 release: http://openresty.org/en/changelog-1011002.html
* Wed Dec 14 2016 Yichun Zhang
- enabled http_geoip_module by default.
* Thu Nov 17 2016 Yichun Zhang
- upgraded OpenResty to 1.11.2.2.
* Fri Aug 26 2016 Yichun Zhang
- use dual number mode in our luajit builds which should usually
be faster for web application use cases.
* Wed Aug 24 2016 Yichun Zhang
- bump OpenResty version to 1.11.2.1.
* Tue Aug 23 2016 zxcvbn4038
- use external packages openresty-zlib and openresty-pcre through dynamic linking.
* Thu Jul 14 2016 Yichun Zhang
- enabled more nginx standard modules as well as threads and file aio.
* Sun Jul 10 2016 makerpm
- initial build for OpenResty 1.9.15.1.
