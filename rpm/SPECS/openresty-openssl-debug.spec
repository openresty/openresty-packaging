Name:               openresty-openssl-debug
Version:            1.0.2k
Release:            1%{?dist}
Summary:            Debug version of the OpenSSL library for OpenResty

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://www.openssl.org/source/openssl-%{version}.tar.gz

Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.0.2h-sess_set_get_cb_yield.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, ElectricFence, perl
Requires:           ElectricFence

BuildRequires:      openresty-zlib-devel >= 1.2.8
Requires:           openresty-zlib >= 1.2.8

AutoReqProv:        no

%define openssl_prefix      %{_usr}/local/openresty-debug/openssl
%define zlib_prefix         /usr/local/openresty/zlib


%description
This is the debug version of the OpenSSL library build for OpenResty uses.


%package devel

Summary:            Debug version of development files for OpenResty's OpenSSL library
Group:              Development/Libraries
Requires:           openresty-openssl-debug

%description devel
Provides C header and static library for the debug version of OpenResty's OpenSSL library. This is the debug version.

%prep
%setup -q -n openssl-%{version}

%patch0 -p1


%build
./config \
    no-threads no-asm \
    shared zlib -d -DPURIFY \
    --openssldir=%{openssl_prefix} \
    --libdir=lib \
    -I%{zlib_prefix}/include \
    -L%{zlib_prefix}/lib \
    -Wl,-rpath,%{zlib_prefix}/lib:%{openssl_prefix}/lib

make %{?_smp_mflags}


%install
make install_sw INSTALL_PREFIX=%{buildroot}

chmod +w %{buildroot}%{openssl_prefix}/lib/*.so
chmod +w %{buildroot}%{openssl_prefix}/lib/*/*.so

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
%attr(0644,root,root) %{openssl_prefix}/openssl.cnf


%files devel
%defattr(-,root,root,-)

%{openssl_prefix}/include/*
%attr(0755,root,root) %{openssl_prefix}/lib/*.a


%changelog
* Sun Mar 19 2017 Yichun Zhang (agentzh)
- upgraded OpenSSL to 1.0.2k.
* Fri Nov 25 2016 Yichun Zhang (agentzh)
- added perl to the BuildRequires list.
* Tue Oct  4 2016 Yichun Zhang (agentzh)
- fixed the rpath of libssl.so (we should have linked against
our own libcrypto.so).
* Sat Sep 24 2016 Yichun Zhang (agentzh)
- upgrade to OpenSSL 1.0.2i.
* Tue Aug 23 2016 zxcvbn4038
- use openresty-zlib instead of the system one.
* Sun Jul 13 2016 makerpm
- initial build for OpenSSL 1.0.2h.
