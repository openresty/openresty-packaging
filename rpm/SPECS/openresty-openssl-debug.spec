Name:               openresty-openssl-debug
Version:            1.0.2h
Release:            5%{?dist}
Summary:            Debug version of the OpenSSL library for OpenResty

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://www.openssl.org/source/openssl-%{version}.tar.gz

Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.0.2h-sess_set_get_cb_yield.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, ElectricFence
Requires:           ElectricFence


%define openssl_prefix      %{_usr}/local/openresty-debug/openssl

%description
This is the debug version of the OpenSSL library build for OpenResty uses.


%package devel

Summary:            development files for OpenResty's OpenSSL library
Group:              Development/Libraries
Requires:           openresty-openssl-debug

%description devel
Provides C header and static library for the debug version of OpenResty's OpenSSL library.

%prep
%setup -q -n openssl-%{version}

%patch0 -p1


%build
./config --prefix=%{openssl_prefix} \
    no-threads no-asm \
    shared -d -DPURIFY

make %{?_smp_mflags}


%install
make install_sw INSTALL_PREFIX=%{buildroot}

chmod +w %{buildroot}%{openssl_prefix}/lib/*.so
chmod +w %{buildroot}%{openssl_prefix}/lib/*/*.so

rm -rf %{buildroot}%{openssl_prefix}/bin
rm -rf %{buildroot}%{openssl_prefix}/ssl

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{openssl_prefix}/lib/*.so*
%attr(0755,root,root) %{openssl_prefix}/lib/*/*.so*


%files devel
%defattr(-,root,root,-)

%{openssl_prefix}/include/*
%{openssl_prefix}/lib/pkgconfig/*
%attr(0755,root,root) %{openssl_prefix}/lib/*.a


%changelog
* Sun Jul 13 2016 makerpm
- initial build for OpenSSL 1.0.2h.
