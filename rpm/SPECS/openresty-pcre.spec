Name:               openresty-pcre
Version:            8.43
Release:            2%{?dist}
Summary:            Perl-compatible regular expression library for OpenResty

Group:              System Environment/Libraries

License:            BSD
URL:                http://www.pcre.org/
Source0:            https://ftp.pcre.org/pub/pcre/pcre-%{version}.tar.bz2

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      ccache, libtool

AutoReqProv:        no

%define pcre_prefix     /usr/local/openresty/pcre


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

export CC="ccache gcc -fdiagnostics-color=always"

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
* Sun Mar 19 2017 Yichun Zhang (agentzh)
- upgraded PCRE to 8.40.
* Sat Sep 24 2016 Yichun Zhang
- disable the C++ support in build. thanks luto.
* Tue Aug 23 2016 zxcvbn4038
- initial build for pcre 8.39.
