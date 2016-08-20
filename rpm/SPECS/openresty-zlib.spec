Name:               openresty-zlib
Version:            1.2.8
Release:            1%{?dist}
Summary:            The zlib compression library for OpenResty

Group:              System Environment/Libraries

# /contrib/dotzlib/ have Boost license
License:            zlib and Boost
URL:                http://www.zlib.net/
Source0:            http://www.zlib.net/zlib-%{version}.tar.xz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      libtool

%define zlib_prefix /usr/local/openresty/zlib

# Do not check openresty files for provides, our internals are not for others.
AutoReqProv:        no

%description
The zlib compression library for use by Openresty ONLY

%package devel

Summary:            Header files and libraries for Zlib development
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
The zlib header files for use by OpenResty ONLY

%prep
%setup -q -n zlib-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS -Wl,-rpath,%{zlib_prefix}/lib -Wl,-z,relro -Wl,-z,now"
./configure --prefix=%{zlib_prefix}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{zlib_prefix}/share
rm -f  %{buildroot}/%{zlib_prefix}/lib/*.la
rm -rf %{buildroot}/%{zlib_prefix}/lib/pkgconfig

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{zlib_prefix}/lib/libz.so*

%files devel
%defattr(-,root,root,-)
%{zlib_prefix}/lib/*.a
%{zlib_prefix}/include/zlib.h
%{zlib_prefix}/include/zconf.h

%changelog
* Wed Aug 10 2016 makerpm
- initial build for zlib 1.2.8 lib

