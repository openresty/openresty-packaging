Name:           perl-Test-LongString
Version:        0.17
Release:        2%{?dist}
Summary:        Tests strings for equality, with more helpful failures
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-LongString/
Source0:        http://www.cpan.org/authors/id/R/RG/RGARCIA/Test-LongString-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
AutoReqProv:    no
BuildRequires:  perl >= 1:5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester)
Requires:       perl(Test::Builder)
Requires:       perl(Test::Builder::Tester)

%description
This module provides some drop-in replacements for the string comparison
functions of Test::More, but which are more suitable when you test against
long strings. If you've ever had to search for text in a multi-line string
like an HTML document, or find specific items in binary data, this is the
module for you.

%prep
%setup -q -n Test-LongString-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes META.json README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun May 21 2017 Yichun Zhang (agentzh) <yichun@openresty.com> 0.17-1
- Specfile autogenerated by cpanspec 1.78.
