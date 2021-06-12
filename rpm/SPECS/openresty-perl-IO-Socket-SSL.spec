%define         _name   IO-Socket-SSL
%define         prefix  /usr/local/openresty-perl
%define         _perl   %{prefix}/bin/perl
%define         sitelib %{prefix}/lib/site_perl

Name:           openresty-perl-IO-Socket-SSL
Version:        2.071
Release:        1%{?dist}
Summary:        Nearly transparent SSL encapsulation for IO::Socket::INET.
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IO-Socket-SSL/
BuildArch:      noarch
Source0:        https://cpan.metacpan.org/authors/id/S/SU/SULLR/%{_name}-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

Requires:       openresty-perl >= 5.24.4
Requires:       openresty-perl-Net-SSLeay >= 1.46
BuildRequires:  openresty-perl >= 5.24.4
BuildRequires:  openresty-perl-devel >= 5.24.4

%description
A perl module

%prep

%setup -q -n %{_name}-%{version}

%build

PERL_MM_USE_DEFAULT=1 %{_perl} Makefile.PL OPTIMIZE="$RPM_OPT_FLAGS" INSTALLDIRS=site \
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
* Thu Jun 10 2021 openresty 2.071-1
- Generated using cpantorpm

