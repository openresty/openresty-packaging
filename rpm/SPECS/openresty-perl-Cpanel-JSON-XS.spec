%define         _name   Cpanel-JSON-XS
%define         prefix  /usr/local/openresty-perl
%define         _perl   %{prefix}/bin/perl
%define         sitelib %{prefix}/lib/site_perl

Name:           openresty-perl-Cpanel-JSON-XS
Version:        4.28
Release:        1%{?dist}
Summary:        cPanel fork of JSON::XS, fast and correct serializing
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Cpanel-JSON-XS/
BuildArch:      %{_arch}
Source0:        https://cpan.metacpan.org/authors/id/R/RU/RURBAN/%{_name}-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

Requires:       openresty-perl >= 5.24.4
BuildRequires:  openresty-perl >= 5.24.4
BuildRequires:  openresty-perl-devel >= 5.24.4

%description
This module converts Perl data structures to JSON and vice versa. Its
primary goal is to be correct and its secondary goal is to be fast.
To reach the latter goal it was written in C.

%prep
%setup -q -n %{_name}-%{version}
chmod -R u+w %{_builddir}/%{_name}-%{version}

if [ -f pm_to_blib ]; then rm -f pm_to_blib; fi

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
%{prefix}/bin/*
%{sitelib}/*

%changelog
* Mon May 9 2022 Yichun Zhang (agentzh) 4.28-1
- upgraded openresty-utils to 4.28.
* Thu May 05 2022 jiahao 4.27-1
- Generated using cpantorpm
