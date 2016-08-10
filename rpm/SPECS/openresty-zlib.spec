Name:						openresty-zlib
Version:				1.2.8
Release:				1%{?dist}
Summary:				The compression and decompression library for OpenResty

Group:					System Environment/Libraries

# /contrib/dotzlib/ have Boost license
License:				zlib and Boost
URL:						http://www.zlib.net/
Source0:				http://www.zlib.net/zlib-%{version}.tar.xz

BuildRoot:			%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	automake, autoconf, libtool

%define openresty_prefix /usr/local/openresty

# Do not check openresty files for provides, our internals are not for others.
AutoReqProv: no

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

%package devel

Summary:				Header files and libraries for Zlib development
Group:					Development/Libraries
Requires:				%{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%package static
Summary: Static libraries for Zlib development
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The zlib-static package includes static libraries needed
to develop programs that use the zlib compression and
decompression library.

%prep
%setup -q -n zlib-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now"
./configure \
  --libdir=%{openresty_prefix}/%{_lib} \
  --includedir=%{openresty_prefix}/include \
  --prefix=%{openresty_prefix}
make %{?_smp_mflags}

%check
make test

%install
make install DESTDIR=%{buildroot}
mv -f %{buildroot}/%{openresty_prefix}/share/man %{buildroot}/%{openresty_prefix}/man
rm -f %{buildroot}/%{openresty_prefix}/%{_lib}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{openresty_prefix}/%{_lib}/libz.so.*

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %{openresty_prefix}/%{_lib}/libz.so
%{openresty_prefix}/%{_lib}/pkgconfig/zlib.pc
%{openresty_prefix}/include/zlib.h
%{openresty_prefix}/include/zconf.h
%{openresty_prefix}/man/man3/zlib.3*

%files static
%defattr(-,root,root,-)
%attr(0755,root,root) %{openresty_prefix}/%{_lib}/libz.a

%changelog

