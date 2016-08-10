Name:       openresty-pcre
Version:    8.39
Release:    1%{?dist}
Summary:    Perl-compatible regular expression library for OpenResty

Group:      System Environment/Libraries

License:    BSD
URL:        http://www.pcre.org/
Source0:    ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-%{version}.tar.bz2

# http://vcs.pcre.org/pcre/code/trunk/pcregrep.c?view=patch&r1=1658&r2=1657&pathrev=1658
Patch0:     patch_1658.diff

BuildRequires:  readline-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  glibc-common
BuildRequires:  libtool
BuildRequires:  make
# perl not used because config.h.generic is pregenerated
# Tests:
BuildRequires:  bash
BuildRequires:  diffutils
BuildRequires:  grep

%define openresty_prefix /usr/local/openresty

# Do not check for provides, our internals are not for others.
AutoReqProv: no

%description
PCRE, Perl-compatible regular expression, library has its own native API, but
a set of wrapper functions that are based on the POSIX API are also supplied
in the libpcreposix library. Note that this just provides a POSIX calling
interface to PCRE: the regular expressions themselves still follow Perl syntax
and semantics.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary:    Static library for %{name}
Group:      Development/Libraries
Requires:   %{name}-devel = %{version}-%{release}

%description static
Library for static linking for %{name}.

%package tools
Summary:    Auxiliary utilities for %{name}
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE capabilities like pcregrep or pcretest.

%prep
%setup -q -n pcre-%{version}
%patch0 -p2

%build
LDFLAGS="-Wl,-rpath,%{openresty_prefix}/%{_lib}" ./configure \
  --prefix=%{openresty_prefix} \
  --libdir=%{openresty_prefix}/%{_lib} \
  --enable-jit \
  --enable-pcretest-libreadline --enable-utf --enable-unicode-properties \
  --enable-pcre8 --enable-pcre16 --enable-pcre32
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mv -f %{buildroot}/%{openresty_prefix}/share/man %{buildroot}/%{openresty_prefix}/man

%check
make %{?_smp_mflags} check VERBOSE=yes

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{openresty_prefix}/%{_lib}/*.so.*
%exclude %{openresty_prefix}/%{_lib}/*.la
%exclude %{openresty_prefix}/share

%files devel
%defattr(-,root,root,-)
#FIX%{openresty_prefix}/%{_lib}/*.so
%{openresty_prefix}/%{_lib}/pkgconfig/*
%{openresty_prefix}/include/*.h
%{openresty_prefix}/man/man1/pcre-config.*
%{openresty_prefix}/man/man3/*
%{openresty_prefix}/bin/pcre-config
%exclude %{openresty_prefix}/%{_lib}/*.so

%files static
%defattr(-,root,root,-)
%{openresty_prefix}/%{_lib}/*.a

%files tools
%defattr(-,root,root,-)
%{openresty_prefix}/bin/pcregrep
%{openresty_prefix}/bin/pcretest
%{openresty_prefix}/man/man1/pcregrep.*
%{openresty_prefix}/man/man1/pcretest.*

%clean
# test

%changelog
