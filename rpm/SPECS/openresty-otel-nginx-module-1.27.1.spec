Name:           openresty-otel-nginx-module-1.27.1
Version:        0.1.1.2
Release:        1%{?dist}
Summary:        OTEL Nginx module for openresty

Group:          Development/Libraries

License:        Apache-2.0 license
URL:            https://github.com/nginxinc/nginx-otel

%define or_version           1.27.1.1

Source0:        nginx-otel-plus-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  gcc, cmake, make, perl
BuildRequires:  openresty-plus-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-saas-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-pcre-devel
BuildRequires:  openresty-plus-core-devel
Requires:       openresty-saas-zlib,openresty-plus-openssl111


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


%build
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
mkdir build
cd build
cmake -DPCRE_ROOT_DIR=%{pcre_prefix} -DNGX_OTEL_NGINX_BUILD_DIR=/usr/local/openresty-plus/build/nginx-1.27.1/objs -DOPENSSL_ROOT_DIR=/usr/local/openresty-plus/openssl111 -DZLIB_ROOT=/opt/openresty-saas/zlib ..
free=`cat /proc/meminfo | grep  "^MemAvailable:" | awk '{printf "%d", $2/1024}'`
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
* Fri Sep 13 2024 Yichun Zhang (agentzh) 0.1.1.2-1
- upgraded openresty-otel-nginx-module to 0.1.1.2.
* Thu Sep 5 2024 Yichun Zhang (agentzh) 0.1.1.1-1
- upgraded openresty-otel-nginx-module to 0.1.1.1.
