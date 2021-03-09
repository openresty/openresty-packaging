Name:           perl-IO-Tty
Version:        1.14
Release:        2%{?dist}
Summary:        Low-level allocate a pseudo-Tty, import constants
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IO-Tty/
Source0:        http://www.cpan.org/authors/id/T/TO/TODDR/IO-Tty-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
AutoReqProv:    no

%description
IO::Tty is used internally by IO::Pty to create a pseudo-tty. You wouldn't
want to use it directly except to import constants, use IO::Pty. For a list
of importable constants, see IO::Tty::Constant.

%prep
%setup -q -n IO-Tty-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make -j`nproc`

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog META.json README.md try
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/IO*
%{_mandir}/man3/*

%changelog
* Tue Jul 07 2020 Yichun Zhang (agentzh) <yichun@openresty.com> 1.14-1
- Specfile autogenerated by cpanspec 1.78.
