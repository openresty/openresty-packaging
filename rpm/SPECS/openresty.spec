Name:           openresty
Version:        1.11.2.3
Release:        1%{?dist}
Summary:        OpenResty, scalable web platform by extending NGINX with Lua

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            https://openresty.org/

Source0:        https://openresty.org/download/openresty-%{version}.tar.gz
Source1:        openresty.init

#Patch0:         openresty-%{version}.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc, make, perl, systemtap-sdt-devel
BuildRequires:  openresty-zlib-devel >= 1.2.11-1
BuildRequires:  openresty-openssl-devel >= 1.0.2k-1
BuildRequires:  openresty-pcre-devel >= 8.40-1
BuildRequires:  GeoIP-devel
Requires:       openresty-zlib >= 1.2.11-1
Requires:       openresty-openssl >= 1.0.2k-1
Requires:       openresty-pcre >= 8.40-1
Requires:       GeoIP

# for /sbin/service
Requires(post):  chkconfig
Requires(preun): chkconfig, initscripts

AutoReqProv:        no

%define orprefix            %{_usr}/local/%{name}
%define zlib_prefix         %{orprefix}/zlib
%define pcre_prefix         %{orprefix}/pcre
%define openssl_prefix      %{orprefix}/openssl


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
Requires:       perl, openresty >= %{version}-%{release}

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


%package opm

Summary:        OpenResty Package Manager
Group:          Development/Tools
Requires:       perl, openresty >= %{version}-%{release}, perl(Digest::MD5)
Requires:       curl, tar, gzip
#BuildRequires:  perl(Digest::MD5)

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description opm
This package provides the client side tool, opm, for OpenResty Pakcage Manager (OPM).


%prep
%setup -q -n "openresty-%{version}"

#%patch0 -p1


%build
./configure \
    --prefix="%{orprefix}" \
    --with-cc-opt="-I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include" \
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
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT' \
    --with-dtrace-probes \
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
ln -sf %{orprefix}/bin/opm %{buildroot}/usr/bin/
ln -sf %{orprefix}/nginx/sbin/nginx %{buildroot}/usr/bin/%{name}

mkdir -p %{buildroot}/etc/init.d
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}/etc/init.d/%{name}

# to silence the check-rpath error
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

/etc/init.d/%{name}
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


%files opm
%defattr(-,root,root,-)

/usr/bin/opm
%{orprefix}/bin/opm
%{orprefix}/site/manifest/
%{orprefix}/site/pod/


%changelog
* Fri Apr 21 2017 Yichun Zhang (agentzh)
- upgrade to the OpenResty 1.11.2.3 release: http://openresty.org/en/changelog-1011002.html
* Sat Dec 24 2016 Yichun Zhang
- init script: explicity specify the runlevels 345.
* Wed Dec 14 2016 Yichun Zhang
- opm missing runtime dependencies curl, tar, and gzip.
- enabled http_geoip_module by default.
* Fri Nov 25 2016 Yichun Zhang
- opm missing runtime dependency perl(Digest::MD5)
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
