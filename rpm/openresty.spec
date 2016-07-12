Name:           openresty
Version:        1.9.15.1
Release:        1%{?dist}
Summary:        Scalable web platform by extending NGINX with Lua

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            https://openresty.org/

Source0:        https://openresty.org/download/openresty-%{version}.tar.gz
Source1: 	openresty.init
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc, make, pcre-devel, zlib-devel, openssl-devel, perl
Requires:       perl, pcre, zlib, openssl

# for /sbin/service
Requires(post):     chkconfig
Requires(preun):    chkconfig, initscripts


%define orprefix    %{_usr}/local/openresty


%description
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
%setup -q


%build
./configure \
    --without-http_rds_json_module \
    --without-http_rds_csv_module \
    --without-lua_rds_parser \
    --with-ipv6 \
    --with-pcre-jit \
    --with-stream \
    --with-stream_ssl_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-luajit-xcflags='-DLUAJIT_ENABLE_LUA52COMPAT' \
    %{?_smp_mflags}

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

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
/usr/bin/resty
/usr/bin/restydoc
/usr/bin/openresty
%{orprefix}/luajit/*
%{orprefix}/lualib/*
%{orprefix}/nginx/html/*
%{orprefix}/nginx/logs/
%{orprefix}/nginx/sbin/*
%{orprefix}/bin/*
%{orprefix}/pod/*
%{orprefix}/resty.index
%config(noreplace) %{orprefix}/nginx/conf/*


%changelog
* Sun Jul 10 2016 makerpm
- initial build for OpenResty 1.9.15.1.
