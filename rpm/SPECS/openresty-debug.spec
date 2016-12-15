Name:           openresty-debug
Version:        1.11.2.2
Release:        3%{?dist}
Summary:        The debug version of OpenResty

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            https://openresty.org/

Source0:        https://openresty.org/download/openresty-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc, make, perl, systemtap-sdt-devel
BuildRequires:  openresty-zlib-devel >= 1.2.8-1
BuildRequires:  openresty-openssl-debug-devel >= 1.0.2j-1
BuildRequires:  openresty-pcre-devel >= 8.39-3
BuildRequires:  GeoIP-devel
Requires:       openresty-zlib >= 1.2.8-1
Requires:       openresty-openssl-debug >= 1.0.2j-1
Requires:       openresty-pcre >= 8.39-3
Requires:       GeoIP

AutoReqProv:        no

%define orprefix            %{_usr}/local/%{name}
%define openssl_prefix      %{orprefix}/openssl
%define zlib_prefix         %{_usr}/local/openresty/zlib
%define pcre_prefix         %{_usr}/local/openresty/pcre


%description
This package contains the debug version of the core server for OpenResty.
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
    --with-debug \
    --with-cc-opt="-I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -O0" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
    --with-pcre-jit \
    --without-http_rds_json_module \
    --without-http_rds_csv_module \
    --without-lua_rds_parser \
    --with-ipv6 \
    --with-stream \
    --with-stream_ssl_module \
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
    --with-http_geoip_module \
    --with-http_gzip_static_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-threads \
    --with-file-aio \
    --with-poll_module \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -O0' \
    --with-dtrace-probes \
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
rm -rf %{buildroot}%{orprefix}/bin/nginx-xml2pod
rm -rf %{buildroot}%{orprefix}/bin/opm
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
%{orprefix}/nginx/tapset/*
%config(noreplace) %{orprefix}/nginx/conf/*


%changelog
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
