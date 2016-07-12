Name:           openresty
Version:        1.9.15.1
Release:        7%{?dist}
Summary:        OpenResty, scalable web platform by extending NGINX with Lua

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            https://openresty.org/


%define         orprefix            %{_usr}/local/openresty
%define         openssl_version     1.0.2h
%define         pcre_version        8.39
%define         zlib_version        1.2.8


Source0:        https://openresty.org/download/openresty-%{version}.tar.gz
Source1:        openresty.init
Source2:        https://www.openssl.org/source/openssl-%{openssl_version}.tar.gz
Source3:        ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{pcre_version}.tar.gz
Source4:        http://zlib.net/zlib-%{zlib_version}.tar.gz

Patch0:         openresty-%{version}-resty_cli_find_bin.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, perl
Requires:       pcre, zlib, openssl
Provides:       openresty-nginx

# for /sbin/service
Requires(post):     chkconfig
Requires(preun):    chkconfig, initscripts


%description
This package contains the core server for OpenResty. Built for production
uses.

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

Summary:        OpenResty command-line utility, resty
Group:          Development/Tools
Requires:       perl, openresty-nginx

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description resty
This package contains the "resty" command-line utility for OpenResty, which
runs OpenResty Lua scripts on the terminal using a headless NGINX behind the
scene.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.


%package doc

Summary:        OpenResty documentation tool, restydoc
Group:          Development/Tools
Requires:       perl
Provides:       restydoc, restydoc-index, md2pod.pl

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description doc
This package contains the official OpenResty documentation index and
the "restydoc" command-line utility for viewing it.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.


%prep
%setup -q
%setup -q -b 2
%setup -q -b 3
%setup -q -b 4

%patch0 -p1


%build
./configure \
    --with-zlib=../zlib-%{zlib_version} \
    --with-openssl=../openssl-%{openssl_version} \
    --with-pcre=../pcre-%{pcre_version} \
    --with-pcre-opt="-DSUPPORT_UTF" \
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
    --with-http_auth_request_module \
    --with-http_sub_module \
    --with-luajit-xcflags='-DLUAJIT_ENABLE_LUA52COMPAT' \
    %{?_smp_mflags}

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{orprefix}/luajit/share/man
rm -rf %{buildroot}%{orprefix}/luajit/lib/libluajit-5.1.a

mkdir -p %{buildroot}/usr/bin
ln -sf %{orprefix}/bin/resty %{buildroot}/usr/bin/
ln -sf %{orprefix}/bin/restydoc %{buildroot}/usr/bin/
ln -sf %{orprefix}/nginx/sbin/nginx %{buildroot}/usr/bin/openresty

mkdir -p %{buildroot}/etc/init.d
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}/etc/init.d/openresty

# to suppress the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%post
/sbin/chkconfig --add %{name}


%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi


%files
%defattr(-,root,root,-)

/etc/init.d/openresty
/usr/bin/openresty
%{orprefix}/luajit/*
%{orprefix}/lualib/*
%{orprefix}/nginx/html/*
%{orprefix}/nginx/logs/
%{orprefix}/nginx/sbin/*
%config(noreplace) %{orprefix}/nginx/conf/*


%files resty
%defattr(-,root,root,-)

/usr/bin/resty
%{orprefix}/bin/resty


%files doc
%defattr(-,root,root,-)

/usr/bin/restydoc
%{orprefix}/bin/restydoc
%{orprefix}/bin/restydoc-index
%{orprefix}/bin/md2pod.pl
%{orprefix}/bin/nginx-xml2pod
%{orprefix}/pod/*
%{orprefix}/resty.index


%changelog
* Sun Jul 10 2016 makerpm
- initial build for OpenResty 1.9.15.1.
