%define or_plus_name    openresty-plus
%define saas_or_prefix  /opt/openresty-saas
%define zlib_prefix     %{saas_or_prefix}/zlib
%define pcre_prefix     %{saas_or_prefix}/pcre
%define openssl_prefix  %{saas_or_prefix}/openssl111


Name:       openresty-saas
Version:    1.19.3.1.3
Release:    1%{?dist}
Summary:    OpenResty Plus for SaaS product clients

Group:      System Environment/Daemons

License:    Proprietary
URL:        http://openresty.com
Source0:    %{or_plus_name}-%{version}.tar.gz


BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl
BuildRequires:  openresty-saas-zlib-devel >= 1.2.11-1
BuildRequires:  openresty-saas-openssl111-devel >= 1.1.1h-1
BuildRequires:  openresty-saas-pcre-devel >= 8.44
BuildRequires:  glibc-devel, texinfo
Requires:       openresty-saas-zlib >= 1.2.11-1
Requires:       openresty-saas-openssl111 >= 1.1.0h-1
Requires:       openresty-saas-pcre >= 8.44

AutoReqProv:    no

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{or_plus_name}-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%description
OpenResty Plus for SaaS product clients.


%prep
%setup -q -n %{or_plus_name}-%{version}


%build
./configure \
    --prefix="%{saas_or_prefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-DNGX_LUA_ABORT_AT_PANIC -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -g3 -O3" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
    --with-pcre-jit \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-stream \
    --with-http_v2_module \
    --with-threads \
    --with-lua_resty_dmi \
    --with-luajit-xcflags="-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -O3 -g3 -DLUAJIT_ENABLE_GC64" \
    --without-lua_resty_memcached_shdict \
    --without-lua_resty_shdict_simple \
    --without-lua_resty_cookie \
    --without-pgmoon \
    --without-lua_resty_balancer \
    --without-lua_resty_utf8_escape \
    --without-lua_resty_charset \
    --without-lua_resty_upstream \
    --without-edge_message_bus \
    --without-edge_routing_platform \
    --without-edge_pki \
    --without-lua_resty_config \
    --without-lua_resty_request_id \
    --without-lua_gd \
    --without-lua_captcha \
    --without-lua_resty_domain_suffix \
    --without-lua_resty_triegen \
    --without-edge_message_bus \
    --without-http_lua_conf \
    --without-http_cache_index \
    --without-http_lua_metrics \
    --without-lmdb \
    --without-tcc \
    --without-lua_resty_maxminddb \
    %{?_smp_mflags}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

pushd %{buildroot}

for f in `find .%{saas_or_prefix}/lualib -type f -name '*.lua'`; do
    LUA_PATH=".%{saas_or_prefix}/luajit/share/luajit-2.1.0-beta3/?.lua;;" .%{saas_or_prefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm -f $f
done

popd

rm -rf %{buildroot}%{saas_or_prefix}/luajit/share/man
rm -f %{buildroot}%{saas_or_prefix}/luajit/lib/libluajit-5.1.a
rm -rf %{buildroot}%{saas_or_prefix}/pod/*
rm -f %{buildroot}%{saas_or_prefix}/resty.index
rm -f %{buildroot}%{saas_or_prefix}/bin/md2pod.pl
rm -f %{buildroot}%{saas_or_prefix}/bin/nginx-xml2pod
rm -f %{buildroot}%{saas_or_prefix}/bin/openresty-plus
rm -f %{buildroot}%{saas_or_prefix}/bin/opm

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%{saas_or_prefix}/bin/resty
%{saas_or_prefix}/site/lualib/
%{saas_or_prefix}/luajit/*
%{saas_or_prefix}/lualib/*
%{saas_or_prefix}/nginx/html/*
%{saas_or_prefix}/nginx/logs/
%{saas_or_prefix}/nginx/sbin/*
%config(noreplace) %{saas_or_prefix}/nginx/conf/*
%{saas_or_prefix}/COPYRIGHT

%changelog
* Sun Dec 20 2020 Yichun Zhang (agentzh) 1.19.3.1.3-1
- upgraded openresty-plus to 1.19.3.1.3.
* Tue Oct 27 2020 Yichun Zhang (agentzh) 1.17.8.2.10-1
- upgraded openresty-plus to 1.17.8.2.10.
* Tue Oct 13 2020 Yichun Zhang (agentzh) 1.17.8.2.8-1
- upgraded openresty-plus to 1.17.8.2.8.
* Fri Oct 9 2020 Yichun Zhang (agentzh) 1.17.8.2.7-1
- upgraded openresty-plus to 1.17.8.2.7.
* Fri Oct 2 2020 Yichun Zhang (agentzh) 1.17.8.2.6-1
- upgraded openresty-plus to 1.17.8.2.6.
* Wed Sep 30 2020 Yichun Zhang (agentzh) 1.17.8.2.4-1
- upgraded openresty-plus to 1.17.8.2.4.

* Wed Sep 02 2020 Johnny Wang (johnny) 1.17.8.2.3-1
- upgraded openresty-plus to 1.17.8.2.3.

* Fri Aug 28 2020 Jiahao Wang (johnny) 1.17.8.2.2-1
- upgraded OpenResty to 1.17.8.2.2.

* Thu Aug 27 2020 Jiahao Wang (johnny) 1.17.8.2.1-1
- upgraded OpenResty to 1.17.8.2.1.

* Wed Sep 04 2019 Jiahao Wang (johnny) 1.15.8.2.2-1
- initial packaging
