Name:               openresty-openssl3
Version:            3.4.1
Release:            1%{?dist}
Summary:            OpenSSL library for OpenResty

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://github.com/openssl/openssl/releases/download/openssl-%{version}/openssl-%{version}.tar.gz

Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-3.4.1-sess_set_get_cb_yield.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, perl
%if ! 0%{?suse_version}
BuildRequires:      perl-IPC-Run, perl-IPC-Cmd, perl-Digest, perl-Digest-SHA
%endif
BuildRequires:      openresty-zlib-devel >= 1.2.11
Requires:           openresty-zlib >= 1.2.11

AutoReqProv:        no

%define openssl_prefix      /usr/local/openresty/openssl3
%define zlib_prefix         /usr/local/openresty/zlib
%global _default_patch_fuzz 1


%description
This OpenSSL library build is specifically for OpenResty uses. It may contain
custom patches from OpenResty.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openssl-%{version}"; \
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

Summary:            Development files for OpenResty's OpenSSL library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
Provides C header and static library for OpenResty's OpenSSL library.


%prep
%setup -q -n openssl-%{version}

%patch0 -p1


%build
./config \
    shared zlib -g \
    --prefix=%{openssl_prefix} \
    --libdir=lib \
    enable-camellia enable-seed enable-rfc3779 \
    enable-cms enable-md2 enable-rc5 \
    enable-weak-ssl-ciphers \
    enable-ssl3 enable-ssl3-method \
    enable-md2 enable-ktls enable-fips\
    -I%{zlib_prefix}/include \
    -L%{zlib_prefix}/lib \
    -Wl,-rpath,%{zlib_prefix}/lib:%{openssl_prefix}/lib

ncpus=`nproc`
if [ "$ncpus" -gt 16 ]; then
    ncpus=16
fi
make CC='ccache gcc -fdiagnostics-color=always' -j$ncpus


%install
make install_sw DESTDIR=%{buildroot}

chmod 0755 %{buildroot}%{openssl_prefix}/lib/*.so*
chmod 0755 %{buildroot}%{openssl_prefix}/lib/*/*.so*

rm -rf %{buildroot}%{openssl_prefix}/bin/c_rehash

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%dir %{openssl_prefix}
%dir %{openssl_prefix}/bin
%dir %{openssl_prefix}/lib
%dir %{openssl_prefix}/lib/engines-3
%dir %{openssl_prefix}/lib/ossl-modules
%attr(0755,root,root) %{openssl_prefix}/bin/openssl
%{openssl_prefix}/lib/libcrypto.so.3
%{openssl_prefix}/lib/libssl.so.3
%{openssl_prefix}/lib/libcrypto.so
%{openssl_prefix}/lib/libssl.so
%{openssl_prefix}/lib/engines-3/*.so
%{openssl_prefix}/lib/ossl-modules/*.so


%files devel
%defattr(-,root,root,-)

%dir %{openssl_prefix}/include
%{openssl_prefix}/include/*
%{openssl_prefix}/lib/*.a
%{openssl_prefix}/lib/pkgconfig/*.pc
%{openssl_prefix}/lib/cmake/OpenSSL/OpenSSLConfig.cmake
%{openssl_prefix}/lib/cmake/OpenSSL/OpenSSLConfigVersion.cmake

%changelog
* Sat Mar 1 2025 Yichun Zhang (agentzh) 3.4.1-1
- upgraded OpenSSL to 3.4.1.
* Sat Sep 14 2024 makerpm 3.0.15
- initial build for OpenSSL 3.0.15
