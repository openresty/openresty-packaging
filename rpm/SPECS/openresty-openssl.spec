Name:               openresty-openssl
Version:            1.0.2h
Release:            5%{?dist}
Summary:            OpenSSL library for OpenResty

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://www.openssl.org/source/openssl-%{version}.tar.gz

Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.0.2h-sess_set_get_cb_yield.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, 
BuildRequires:			openresty-zlib-devel >= 1.2.8
Requires:						openresty-zlib >= 1.2.8

%define openresty_prefix /usr/local/openresty

# Do not check openresty files for provides, our internals are not for others.
AutoReqProv: no

%description
This OpenSSL library build is specifically for OpenResty uses. It may contain
custom patches from OpenResty.


%package devel

Summary:            Development files for OpenResty's OpenSSL library
Group:              Development/Libraries
Requires:           openresty-openssl

%description devel
Provides C header and static library for OpenResty's OpenSSL library.

%prep
%setup -q -n openssl-%{version}
%patch0 -p1


%build
./config --openssldir=%{_prefix} no-threads shared zlib -g \
-I%{openresty_prefix}/include \
-L%{openresty_prefix}/%{_lib} \
-Wl,-rpath,%{openresty_prefix}/%{_lib}
make %{?_smp_mflags}


%install
make install_sw INSTALL_PREFIX=%{buildroot}

chmod +w %{buildroot}%{_prefix}/%{_lib}/*.so
chmod +w %{buildroot}%{_prefix}/%{_lib}/*/*.so

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{openresty_prefix}/bin/openssl
%attr(0755,root,root) %{openresty_prefix}/%{_lib}/*.so*
%attr(0755,root,root) %{openresty_prefix}/%{_lib}/*/*.so*
%exclude %{openresty_prefix}/bin/c_rehash
%exclude %{openresty_prefix}/misc
%exclude %{openresty_prefix}/openssl.cnf

%files devel
%defattr(-,root,root,-)

%{openresty_prefix}/include/*
%{openresty_prefix}/%{_lib}/pkgconfig/*
%attr(0755,root,root) %{openresty_prefix}/%{_lib}/*.a


%changelog
* Sun Jul 13 2016 makerpm
- initial build for OpenSSL 1.0.2h.lib
