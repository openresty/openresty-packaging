Name:               openresty-pcre
Version:            8.39
Release:            1%{?dist}
Summary:            Perl-compatible regular expression library for OpenResty

Group:              System Environment/Libraries

License:            BSD
URL:                http://www.pcre.org/
Source0:            ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{version}.tar.bz2

BuildRequires:      libtool

%define pcre_prefix /usr/local/openresty/pcre

# Do not check for provides, our internals are not for others.
AutoReqProv:        no

%description
Perl-compatible regular expression library for use by OpenResty ONLY

%package devel
Summary:            Development files for %{name}
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
Development files for Perl-compatible regular expression library for use by OpenResty ONLY

%prep
%setup -q -n pcre-%{version}

%build
LDFLAGS="-Wl,-rpath,%{pcre_prefix}/lib" ./configure \
  --prefix=%{pcre_prefix} \
  --enable-jit \
  --enable-utf \
  --enable-unicode-properties \
  --enable-pcre8
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{pcre_prefix}/bin
rm -rf %{buildroot}/%{pcre_prefix}/share
rm -f  %{buildroot}/%{pcre_prefix}/lib/*.la
rm -f  %{buildroot}/%{pcre_prefix}/lib/*pcrecpp*
rm -f  %{buildroot}/%{pcre_prefix}/lib/*pcreposix*
rm -rf %{buildroot}/%{pcre_prefix}/lib/pkgconfig

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{pcre_prefix}/lib/*.so*

%files devel
%defattr(-,root,root,-)
%{pcre_prefix}/lib/*.a
%{pcre_prefix}/include/*.h

%changelog
* Wed Aug 10 2016 makerpm
- initial build for pcre 8.3.9 lib

