Name:               openresty-openssl111
Version:            1.1.1l
Release:            1%{?dist}
Summary:            OpenSSL library for OpenResty

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://www.openssl.org/source/openssl-%{version}.tar.gz

#Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.1e-sess_set_get_cb_yield.patch
Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.1f-sess_set_get_cb_yield.patch
#Patch1:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.0j-parallel_build_fix.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, perl
BuildRequires:      openresty-zlib-devel >= 1.2.11
Requires:           openresty-zlib >= 1.2.11

AutoReqProv:        no

%define openssl_prefix      /usr/local/openresty/openssl111
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
#%patch1 -p1


%build
./config \
    shared zlib -g3 \
    enable-camellia enable-seed enable-rfc3779 \
    enable-cms enable-md2 enable-rc5 \
    enable-weak-ssl-ciphers \
    enable-ssl3 enable-ssl3-method \
    --prefix=%{openssl_prefix} \
    --libdir=lib \
    -I%{zlib_prefix}/include \
    -L%{zlib_prefix}/lib \
    -Wl,-rpath,%{zlib_prefix}/lib:%{openssl_prefix}/lib

make CC='ccache gcc -fdiagnostics-color=always' -j`nproc`


%install
make install_sw DESTDIR=%{buildroot}

chmod 0755 %{buildroot}%{openssl_prefix}/lib/*.so*
chmod 0755 %{buildroot}%{openssl_prefix}/lib/*/*.so*

rm -rf %{buildroot}%{openssl_prefix}/bin/c_rehash
rm -rf %{buildroot}%{openssl_prefix}/lib/pkgconfig
rm -rf %{buildroot}%{openssl_prefix}/misc

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{openssl_prefix}/bin/openssl
%attr(0755,root,root) %{openssl_prefix}/lib/*.so*
%attr(0755,root,root) %{openssl_prefix}/lib/*/*.so*


%files devel
%defattr(-,root,root,-)

%{openssl_prefix}/include/*
%{openssl_prefix}/lib/*.a


%changelog
* Tue May 11 2021 Jiahao Wang 1.1.1k-1
- upgraded OpenSSL to 1.1.1k.
* Thu Dec 10 2020 Yichun Zhang (agentzh) 1.1.1i-1
- upgraded OpenSSL to 1.1.1i.
* Mon May 14 2018 Yichun Zhang (agentzh) 1.1.0h-1
- upgraded openresty-openssl to 1.1.0h.
* Thu Apr 19 2018  Yichun Zhang (agentzh) 1.0.2n-1
- upgraded openssl to 1.0.2n.
* Sun Mar 19 2017 Yichun Zhang (agentzh)
- upgraded OpenSSL to 1.0.2k.
* Fri Nov 25 2016 Yichun Zhang (agentzh)
- added perl to the BuildRequires list.
* Tue Oct  4 2016 Yichun Zhang (agentzh)
- fixed the rpath of libssl.so (we should have linked against
our own libcrypto.so).
* Sat Sep 24 2016 Yichun Zhang (agentzh)
- upgrade to OpenSSL 1.0.2i.
* Tue Aug 23 2016 zxcvbn4038 1.0.2k
- use openresty-zlib instead of the system one.
* Wed Jul 13 2016 makerpm 1.0.2h
- initial build for OpenSSL 1.0.2h.
