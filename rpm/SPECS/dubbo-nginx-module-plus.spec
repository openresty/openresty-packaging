Name:           dubbo-nginx-module-plus-NGINX_VERSION
Version:        1.0.2.1
Release:        1%{?dist}
Summary:        multiple upstream nginx module

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

%define or_version           OPENRESTY_VERSION
%define ngx_version          NGINX_VERSION
%define ngx_multi_upstream_version        1.2.0.1

Source0:        mod_dubbo-%{version}.tar.gz
Source1:        ngx_multi_upstream_module-%{ngx_multi_upstream_version}.tar.gz
Source2:        https://openresty.org/download/openresty-%{or_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl
BuildRequires:  openresty-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-pcre-devel

AutoReqProv:        no

%define or_prefix          /usr/local/openresty
%define zlib_prefix         %{or_prefix}/zlib
%define pcre_prefix         %{or_prefix}/pcre
%define openssl_prefix      %{or_prefix}/openssl111
%define lua_lib_dir         %{or_prefix}/site/lualib


%description
multiple upstream nginx module.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/mod_dubbo-%{version}"; \
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

%prep
%setup -q -n "mod_dubbo-%{version}"
tar xzf %{SOURCE1}
tar xzf %{SOURCE2}


%build
cd openresty-%{or_version}/
cd bundle/nginx-%{ngx_version}
cat ../../../ngx_multi_upstream_module-%{ngx_multi_upstream_version}/nginx-%{ngx_version}.patch | patch -p1
cd ../..

./configure \
    --prefix="%{or_prefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -O3" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
    --with-compat --with-threads \
    --add-dynamic-module=../ \
    --add-dynamic-module=../ngx_multi_upstream_module-%{ngx_multi_upstream_version}

make -C build/nginx-*/ modules -j`nproc`


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{or_prefix}/nginx/modules

cd openresty-*/
install -m755 build/nginx-*/objs/*.so %{buildroot}%{or_prefix}/nginx/modules

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{or_prefix}/nginx/modules/ngx_http_dubbo_module.so
%{or_prefix}/nginx/modules/ngx_http_multi_upstream_module.so
%{or_prefix}/nginx/modules/ngx_stream_multi_upstream_module.so


%changelog
* Wed Nov 20 2024 Yichun Zhang (agentzh) 1.0.2.1-1
- upgraded dubbo-nginx-module-plus to 1.0.2.1.
