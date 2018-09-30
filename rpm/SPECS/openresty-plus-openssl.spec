Name:               openresty-plus-openssl
Version:            1.0.2n
Release:            2%{?dist}
Summary:            OpenSSL library for OpenResty Plus

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://www.openssl.org/source/openssl-%{version}.tar.gz

Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.0.2h-sess_set_get_cb_yield.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, perl
BuildRequires:      openresty-zlib-devel >= 1.2.11
Requires:           openresty-zlib >= 1.2.11

AutoReqProv:        no

%define openssl_prefix      /usr/local/openresty-plus/openssl
%define zlib_prefix         /usr/local/openresty/zlib
%global _default_patch_fuzz 1


%description
This OpenSSL library build is specifically for OpenResty Plus uses. It may contain
custom patches from OpenResty Plus.


%package devel

Summary:            Development files for OpenResty Plus's OpenSSL library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
Provides C header and static library for OpenResty Plus's OpenSSL library.

%prep
%setup -q -n openssl-%{version}

%patch0 -p1


%build
./config \
    no-threads shared zlib -g3 \
    --openssldir=%{openssl_prefix} \
    --libdir=lib \
    -I%{zlib_prefix}/include \
    -L%{zlib_prefix}/lib \
    -Wl,-rpath,%{zlib_prefix}/lib:%{openssl_prefix}/lib

make %{?_smp_mflags}


%install
make install_sw INSTALL_PREFIX=%{buildroot}

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
%attr(0644,root,root) %{openssl_prefix}/openssl.cnf


%files devel
%defattr(-,root,root,-)

%{openssl_prefix}/include/*
%{openssl_prefix}/lib/*.a


%changelog
* Tue May 15 2018 Yichun Zhang (agentzh)
- initial version.
