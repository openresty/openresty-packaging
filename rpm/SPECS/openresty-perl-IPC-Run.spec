%define         _name IPC-Run
%define         prefix /usr/local/openresty-perl
%define         _perl   %{prefix}/bin/perl
%define         sitelib %{prefix}/lib/site_perl

Name:           openresty-perl-IPC-Run
Version:        20200505.0
Release:        1%{?dist}
Summary:        system() and background procs w/ piping, redirs, ptys (Unix, Win32)
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/IPC-Run/
BuildArch:      noarch
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/%{_name}-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

Requires:       openresty-perl-IO-Tty >= 1.08
BuildRequires:  openresty-perl >= 5.24.4
BuildRequires:  openresty-perl-Readonly
Requires:       openresty-perl >= 5.24.4

%description
IPC::Run allows you to run and interact with child processes using files,
pipes, and pseudo-ttys. Both system()-style and scripted usages are
supported and may be mixed. Likewise, functional and OO API styles are both
supported and may be mixed.

This build is specifically for OpenResty uses.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{_name}-%{version}"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%endif

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
* Mon Feb 08 2021 jiahao 20200505.0-1
- Generated using cpantorpm.
