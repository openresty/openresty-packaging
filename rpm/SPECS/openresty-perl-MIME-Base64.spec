%define         _name   MIME-Base64
%define         prefix  /usr/local/openresty-perl
%define         _perl   %{prefix}/bin/perl
%define         sitelib %{prefix}/lib/site_perl


Name:           openresty-perl-MIME-Base64
Version:        3.16
Release:        1%{?dist}
Summary:        Encoding and decoding of base64 strings
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MIME-Base64/
BuildArch:      %{_arch}
Source0:        https://cpan.metacpan.org/authors/id/C/CA/CAPOEIRAB/%{_name}-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

Requires:       openresty-perl >= 5.24.4
BuildRequires:  openresty-perl >= 5.24.4
BuildRequires:  openresty-perl-devel >= 5.24.4


%description
This module provides functions to encode and decode strings into and from
the base64 encoding specified in RFC 2045 - MIME (Multipurpose Internet
Mail Extensions). The base64 encoding is designed to represent arbitrary
sequences of octets in a form that need not be humanly readable. A
65-character subset ([A-Za-z0-9+/=]) of US-ASCII is used, enabling 6 bits
to be represented per printable character.

%prep

%setup -q -n %{_name}-%{version}

%build

%{_perl} Makefile.PL OPTIMIZE="$RPM_OPT_FLAGS" INSTALLDIRS=site \
    INSTALLSITEBIN=%{prefix}/bin INSTALLSITESCRIPT=%{prefix}/bin \
    INSTALLSCRIPT=%{prefix}/bin

make -j`nproc`


%install

rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

rm -rf "%{buildroot}%{prefix}/man"

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%clean

rm -rf $RPM_BUILD_ROOT

%files

%defattr(-,root,root,-)
%{sitelib}/*

%changelog
* Thu Jun 10 2021 openresty 3.16-1
- Generated using cpantorpm

