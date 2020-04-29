Name:               openresty-zlib
Version:            1.2.11
Release:            3%{?dist}
Summary:            The zlib compression library for OpenResty

Group:              System Environment/Libraries

# /contrib/dotzlib/ have Boost license
License:            zlib and Boost
URL:                http://www.zlib.net/
Source0:            http://www.zlib.net/zlib-%{version}.tar.xz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      libtool

AutoReqProv:        no

%define zlib_prefix     /usr/local/openresty/zlib


%description
The zlib compression library for use by Openresty ONLY


%package devel

Summary:            Development files for OpenResty's zlib library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty's zlib library.


%prep
%setup -q -n zlib-%{version}


%build
./configure --prefix=%{zlib_prefix}
make %{?_smp_mflags} CFLAGS='-O3 -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    SFLAGS='-O3 -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    > /dev/stderr


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{zlib_prefix}/share
rm -f  %{buildroot}/%{zlib_prefix}/lib/*.la
rm -rf %{buildroot}/%{zlib_prefix}/lib/pkgconfig


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
* Fri Jul 14 2017 Yichun Zhang 1.2.11-3
- bugfix: we did not enable debuginfo in the shared library files.
* Sat May 20 2017 Yichun Zhang 1.2.11-2
- added debuginfo.
* Sun Mar 19 2017 Yichun Zhang (agentzh)
- upgraded zlib to 1.2.11.
* Wed Aug 23 2016 zxcvbn4038
- initial build for zlib 1.2.8.
