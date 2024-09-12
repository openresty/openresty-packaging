Name:           openresty-otel-nginx-module-NGINX_VERSION
Version:        0.1.1.1
Release:        2%{?dist}
Summary:        OTEL Nginx module for openresty

Group:          Development/Libraries

License:        Apache-2.0 license
URL:            https://github.com/nginxinc/nginx-otel

%define or_version           OPENRESTY_VERSION

Source0:        nginx-otel-plus-%{version}.tar.gz
Source1:        https://openresty.org/download/openresty-%{or_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp, procps-ng
BuildRequires:  ccache, gcc, cmake, make, perl,c-ares, c-ares-devel
BuildRequires:  openresty-plus-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-saas-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-pcre-devel
Requires:       openresty-saas-zlib,openresty-plus-openssl111,c-ares


AutoReqProv:        no

%define or_prefix          /usr/local/openresty-plus
%define zlib_prefix        /opt/openresty-saas/zlib
%define pcre_prefix        /usr/local/openresty/pcre
%define openssl_prefix     /usr/local/openresty-plus/openssl111
%define lua_lib_dir        %{or_prefix}/site/lualib
%define NGX_CC_OPT         -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -O3
%define NGX_LD_OPT         -L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib


%description
Coroutine implemented using ucontext API.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/nginx-otel-plus-%{version}"; \
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
%setup -q -n "nginx-otel-plus-%{version}"
tar xzf %{SOURCE1}


%build
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
cd openresty-%{or_version}/
./configure \
    --prefix="%{or_prefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="%{NGX_CC_OPT}" \
    --with-ld-opt="%{NGX_LD_OPT}" \
    --with-compat --with-threads \
    --with-http_v2_module \
    --with-threads --with-compat --with-stream --with-http_ssl_module --with-stream_ssl_module \
    -j`nproc`
cd ..

mkdir build
cd build
cmake -DNGX_OTEL_NGINX_BUILD_DIR=../openresty-%{or_version}/build/nginx-NGINX_VERSION/objs -DOPENSSL_ROOT_DIR=/usr/local/openresty-plus/openssl111 -DZLIB_ROOT=/opt/openresty-saas/zlib -D "CMAKE_C_FLAGS=%{NGX_CC_OPT}" -D "CMAKE_CXX_FLAGS=%{NGX_CC_OPT}" -D "CMAKE_MODULE_LINKER_FLAGS=%{NGX_LD_OPT}" ..
free=`free -m|grep -E '^Mem'|head -n1|awk '{print $NF}'`
ncpus=`nproc`
max_jobs=$(( $free / 900 ))
# echo "max jobs: $max_jobs"
if [ "$max_jobs" -gt "$ncpus" ]; then
    max_jobs=$ncpus
fi
make -j$max_jobs

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{or_prefix}/nginx/modules

install -m755 build/ngx_otel_module.so %{buildroot}%{or_prefix}/nginx/modules

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{or_prefix}/nginx/modules/ngx_otel_module.so


%changelog
* Thu Sep 5 2024 Yichun Zhang (agentzh) 0.1.1.1-1
- upgraded openresty-otel-nginx-module to 0.1.1.1.
* Wed Sep 4 2024 Yichun Zhang (agentzh) 0.1.1.0-1
- upgraded openresty-otel-nginx-module to 0.1.0.1.
