Name:           perl-Test-Simple
Version:        1.302175
Release:        4%{?dist}
Summary:        Basic utilities for writing tests
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Simple/
Source0:        http://www.cpan.org/authors/id/E/EX/EXODIST/Test-Simple-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
AutoReqProv:    no
BuildRequires:  perl >= 0:5.006002
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Scalar::Util) >= 1.13
BuildRequires:  perl(Storable)
BuildRequires:  perl(utf8)
Requires:       perl(File::Spec)
Requires:       perl(File::Temp)
Requires:       perl(Scalar::Util) >= 1.13
Requires:       perl(Storable)
Requires:       perl(utf8)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl(Test::Tester)
Provides:       perl(Test::More)
Provides:       perl(Test::Simple)
Provides:       perl(Test::Builder)

%description
** If you are unfamiliar with testing read Test::Tutorial first! **

%prep
%setup -q -n Test-Simple-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make -j`nproc`

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
%doc appveyor.yml Changes cpanfile dist.ini examples LICENSE META.json README README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Jul 07 2020 Yichun Zhang (agentzh) <yichun@openresty.com> 1.302175-1
- Specfile autogenerated by cpanspec 1.78.
