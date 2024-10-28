Name:           coro-nginx-module-1.25.3
Version:        0.0.13
Release:        1%{?dist}
Summary:        Coroutine implemented using ucontext API

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

%define or_version     1.25.3.1

Source0:        coro-nginx-module-%{version}.tar.gz
Source1:        openresty-%{or_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl
BuildRequires:  openresty-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-pcre-devel
BuildRequires:  openresty-elf-loader-devel
BuildRequires:  openresty-libcco-devel
BuildRequires:  openresty-elfutils-devel
Requires:       openresty-elf-loader, openresty-libcco, openresty-elfutils


AutoReqProv:        no

%define prefix             /usr/local/openresty-coro-nginx-module
%define or_prefix          /usr/local/openresty
%define zlib_prefix         %{or_prefix}/zlib
%define pcre_prefix         %{or_prefix}/pcre
%define openssl_prefix      %{or_prefix}/openssl111
%define cco_prefix         /usr/local/libcco
%define elf_loader_prefix  /usr/local/elf-loader
%define elfutils_prefix    /usr/local/openresty-elfutils

%description
Coroutine implemented using ucontext API.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/coro-nginx-module-%{version}"; \
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


%package devel
Summary:            Development files for %{name}
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Development files for %{name}.


%prep
%setup -q -n "coro-nginx-module-%{version}"
tar xzf %{SOURCE1}


%build
cd openresty-*/
./configure \
    --prefix="%{prefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-DNGX_HTTP_CORO_USE_FREE_LISTS -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -I%{elf_loader_prefix}/include -I%{cco_prefix}/include -I%{elfutils_prefix}/include -O3" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -L%{elfutils_prefix}/lib -L%{elf_loader_prefix}/lib -L%{cco_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib:%{elfutils_prefix}/lib:%{elf_loader_prefix}/lib:%{cco_prefix}/lib" \
    --with-compat \
    --add-dynamic-module=../ \
    -j`nproc`

make -C build/nginx-*/ modules -j`nproc`


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{prefix}/lib
mkdir -p %{buildroot}%{prefix}/include
cd openresty-*/
install -m755 build/nginx-*/objs/*.so %{buildroot}%{prefix}/lib/
install -m644 ../src/api/*.h %{buildroot}%{prefix}/include/


# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{prefix}/lib/ngx_http_coro_module.so


%files devel
%defattr(-,root,root)
%dir %{prefix}/include
%{prefix}/include/*.h


%changelog
* Mon Oct 28 2024 Yichun Zhang (agentzh) 0.0.13-1
- upgraded coro-nginx-module to 0.0.13.
* Mon Oct 28 2024 Yichun Zhang (agentzh) 0.0.12-1
- upgraded coro-nginx-module to 0.0.12.
* Mon Oct 28 2024 Yichun Zhang (agentzh) 0.0.13-1
- upgraded coro-nginx-module to 0.0.13.
* Tue Oct 15 2024 Yichun Zhang (agentzh) 0.0.12-1
- upgraded coro-nginx-module to 0.0.12.
* Mon Oct 14 2024 Yichun Zhang (agentzh) 0.0.11-1
- upgraded coro-nginx-module to 0.0.11.
* Mon Oct 7 2024 Yichun Zhang (agentzh) 0.0.10-1
- upgraded coro-nginx-module to 0.0.10.
* Mon Apr 1 2024 Yichun Zhang (agentzh) 0.0.9-1
- upgraded coro-nginx-module to 0.0.9.
* Sat Mar 23 2024 Yichun Zhang (agentzh) 0.0.8-1
- upgraded coro-nginx-module to 0.0.8.
* Fri Mar 22 2024 Yichun Zhang (agentzh) 0.0.7-1
- upgraded coro-nginx-module to 0.0.7.
* Wed Apr 5 2023 Yichun Zhang (agentzh) 0.0.5-1
- upgraded coro-nginx-module to 0.0.5.
* Wed Apr 5 2023 Yichun Zhang (agentzh) 0.0.4-1
- upgraded coro-nginx-module to 0.0.4.
* Thu Mar 30 2023 Yichun Zhang (agentzh) 0.0.3-1
- upgraded coro-nginx-module to 0.0.3.
* Thu Mar 30 2023 Hui Wang 0.0.1-1
- initial build for coro-nginx-module.
