%define         _name   Net-SSLeay
%define         prefix  /usr/local/openresty-perl
%define         _perl   %{prefix}/bin/perl
%define         sitelib %{prefix}/lib/site_perl

Name:           openresty-perl-Net-SSLeay
Version:        1.90
Release:        1%{?dist}
Summary:        Perl extension for using OpenSSL
License:        Artistic 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Net-SSLeay/
BuildArch:      %{_arch}
Source0:        https://cpan.metacpan.org/authors/id/C/CH/CHRISN/%{_name}-%{version}.tar.gz


AutoReqProv:    no
AutoReq:        no
AutoProv:       no

Requires:       openresty-perl >= 5.24.4
Requires:       openresty-openssl111
BuildRequires:  openresty-perl >= 5.24.4
BuildRequires:  openresty-perl-devel >= 5.24.4
BuildRequires:  openresty-openssl111
BuildRequires:  openresty-openssl111-devel


%description
A perl module

%prep

%setup -q -n %{_name}-%{version}

%build

PERL_MM_OPT='LD="ccache gcc -Wl,-rpath,/usr/local/openresty/openssl111/lib -L/usr/local/openresty/openssl111/lib" LIBS="-lssl -lcrypto -lz"' \
PERL_MM_USE_DEFAULT=1 \
%{_perl} Makefile.PL OPTIMIZE="$RPM_OPT_FLAGS" INSTALLDIRS=site \
    INSTALLSITEBIN=%{prefix}/bin INSTALLSITESCRIPT=%{prefix}/bin \
    INSTALLSCRIPT=%{prefix}/bin \
    INC=-I/usr/local/openresty/openssl111/include \

make -j`nproc`

%install

rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

rm -rf "%{buildroot}%{prefix}/man"

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

export QA_RPATHS=$[ 0x0002 ]

%clean

rm -rf $RPM_BUILD_ROOT

%files

%defattr(-,root,root,-)
%{sitelib}/*

%changelog
* Thu Jun 10 2021 openresty 1.90-1
- Generated using cpantorpm

