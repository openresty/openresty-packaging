%define         _name   B-C
%define         prefix  /usr/local/openresty-perl
%define         _perl   %{prefix}/bin/perl
%define         sitelib %{prefix}/lib/site_perl

Name:           openresty-perl-B-C
Version:        1.57
Release:        3%{?dist}
Summary:        Perl compiler
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/B-C/
BuildArch:      %{_arch}
Source0:        https://cpan.metacpan.org/authors/id/R/RU/RURBAN/%{_name}-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

Requires:       openresty-perl >= 5.24.4-7
Requires:       openresty-perl-B-Flags >= 0.17-3
Requires:       openresty-perl-IPC-Run
Requires:       openresty-perl-Opcodes
BuildRequires:  openresty-perl >= 5.24.4-7
BuildRequires:  openresty-perl-B-Flags >= 0.17-3
BuildRequires:  openresty-perl-IPC-Run
BuildRequires:  openresty-perl-Opcodes
BuildRequires:  openresty-perl-devel >= 5.24.4-7

%description
This compiler backend takes Perl source and generates C source code
corresponding to the internal structures that perl uses to run your
program. When the generated C source is compiled and run, it cuts out the
time which perl would have taken to load and parse your program into its
internal semi-compiled form. That means that compiling with this backend
will not help improve the runtime execution speed of your program but may
improve the start-up time. Depending on the environment in which your
program runs this may be either a help or a hindrance.

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

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages

%global __brp_mangle_shebangs_exclude_from *
%endif

%if 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
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
%{prefix}/bin/*
%{sitelib}/*

%changelog
* Thu Oct 27 2022 Jiahao Wang 1.57-2
- removed unnecessary -D option from openresty-perl.
* Mon Feb 08 2021 jiahao 1.57-1
- Generated using cpantorpm.
