Name:           perl-Lemplate
Version:        0.07
Release:        5%{?dist}
Summary:        Lemplate Perl module
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Lemplate/
Source0:        http://www.cpan.org/authors/id/A/AG/AGENT/Lemplate-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 1:v5.8.1
BuildRequires:  perl(ExtUtils::MakeMaker)
#BuildRequires:  perl(File::Find::Rule)
BuildRequires:  perl(Template)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(IPC::Run3)
BuildRequires:  perl(Filter::Util::Call)
#Requires:       perl(File::Find::Rule)
Requires:       perl(Template)
#Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Lemplate parses TT2 templates using the TT2 Perl framework, but with a
twist. Instead of compiling the templates into Perl code, it compiles them
into Lua that can run on OpenResty.

%prep
%setup -q -n Lemplate-%{version}

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
%doc Changes Install LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*
/usr/bin/lemplate
/usr/share/man/man1/lemplate.1.gz

%changelog
* Thu Oct 13 2016 Yichun Zhang (agentzh) <agentzh@gmail.com> 0.07-5
- No longer require a particular perl version.
* Fri Jul 15 2016 Yichun Zhang (agentzh) <agentzh@gmail.com> 0.04-1
- Specfile autogenerated by cpanspec 1.78.