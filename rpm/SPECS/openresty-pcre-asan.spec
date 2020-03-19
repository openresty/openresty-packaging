Name:               openresty-pcre-asan
Version:            8.44
Release:            1%{?dist}
Summary:            Clang AddressSanitizer version of the Perl-compatible regular expression library for OpenResty

Group:              System Environment/Libraries

License:            BSD
URL:                http://www.pcre.org/
Source0:            https://ftp.pcre.org/pub/pcre/pcre-%{version}.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      ccache, libtool, clang

AutoReqProv:        no

%define pcre_prefix     /usr/local/openresty-asan/pcre

%if 0%{?el6}
%undefine _missing_build_ids_terminate_build
%endif

#%if 0%{?fedora} >= 28
#BuildRequires:      compiler-rt
#%endif


%description
Perl-compatible regular expression library for use by OpenResty ONLY.
This is the clang AddressSanitizer version.


%package devel
Summary:            Development files for %{name}
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Development files for Perl-compatible regular expression library for use by OpenResty ONLY.
This is the clang AddressSanitizer version.


%prep
%setup -q -n pcre-%{version}


%build
export CC="ccache clang -fsanitize=address -fcolor-diagnostics"
export CFLAGS="-O1 -fno-omit-frame-pointer -g"
export ASAN_OPTIONS=detect_leaks=0

./configure \
  --prefix=%{pcre_prefix} \
  --libdir=%{pcre_prefix}/lib \
  --disable-cpp \
  --enable-jit \
  --enable-utf \
  --enable-unicode-properties

make %{?_smp_mflags} V=1 > /dev/stderr


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{pcre_prefix}/bin
rm -rf %{buildroot}/%{pcre_prefix}/share
rm -f  %{buildroot}/%{pcre_prefix}/lib/*.la
rm -f  %{buildroot}/%{pcre_prefix}/lib/*pcrecpp*
rm -f  %{buildroot}/%{pcre_prefix}/lib/*pcreposix*
rm -rf %{buildroot}/%{pcre_prefix}/lib/pkgconfig


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
* Mon May 14 2018 Yichun Zhang (agentzh) 8.42-1
- upgraded openresty-pcre to 8.42.
* Thu Nov 2 2017 Yichun Zhang (agentzh)
- upgraded PCRE to 8.41.
* Sat Jul 15 2017 Yichun Zhang (agentzh) 8.40-3
- fixed changelog dates.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 8.40-2
- fixed spec for CentOS 6 regarding missing build id issues.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 8.40-1
- initial build for PCRE 8.40.
