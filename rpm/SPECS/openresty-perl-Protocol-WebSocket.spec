%define         _name   Protocol-WebSocket
%define         prefix  /usr/local/openresty-perl
%define         _perl   %{prefix}/bin/perl
%define         sitelib %{prefix}/lib/site_perl


Name:           openresty-perl-Protocol-WebSocket
Version:        0.26
Release:        1%{?dist}
Summary:        WebSocket protocol
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Protocol-WebSocket/
BuildArch:      noarch
Source0:        https://cpan.metacpan.org/authors/id/V/VT/VTI/%{_name}-%{version}.tar.gz


AutoReqProv:    no
AutoReq:        no
AutoProv:       no

Requires:       openresty-perl >= 5.24.4
BuildRequires:  openresty-perl >= 5.24.4
BuildRequires:  openresty-perl-devel >= 5.24.4
BuildRequires:  openresty-perl-Module-Build-Tiny

%description
Client/server WebSocket message and frame parser/constructor. This module
does not provide a WebSocket server or client, but is made for using in
http servers or clients to provide WebSocket support.

%prep

%setup -q -n %{_name}-%{version}

%build

%{_perl} Build.PL optimize="$RPM_OPT_FLAGS" \
    --installdirs site \
    --install_path script=%{prefix}/bin --install_path %{prefix}/bin
./Build

%install

rm -rf $RPM_BUILD_ROOT
./Build install --destdir=$RPM_BUILD_ROOT --create_packlist=0
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
* Sun Jun 27 2021 openresty 0.26-1
- Generated using cpantorpm

