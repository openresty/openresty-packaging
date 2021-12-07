%global prefix      /usr/local/openresty-perl
%global privlib     %{prefix}/share/perl5
%global archlib     %{prefix}/lib/perl5

Name:           openresty-perl
Version:        5.24.4
Release:        3%{?dist}
Summary:        OpenResty's fork of Perl programming language
Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic)
URL:            http://www.perl.org/
Source0:        https://www.cpan.org/src/5.0/perl-%{version}.tar.gz
Patch0:         perl-pp-Guard-fix-for-really-old-bug-in-glibc-libcrypt.patch
BuildRequires:  ccache, gcc
BuildRequires:  gawk, sed
BuildRequires:  procps
BuildRequires:  zlib-devel
AutoReqProv:    0

%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications are system
administration utilities and web programming.  A large proportion of
the CGI scripts on the web are written in Perl.  You need the perl
package installed on your system so that your system can handle Perl
scripts.

Install this package if you want to program in Perl or enable your
system to handle Perl scripts.

This Perl build is specifically for OpenResty uses.

%package devel
Summary: Perl programming Language - development headers
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description devel
Development headers for the OpenResty's fork of Perl.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/perl-%{version}"; \
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
%setup -q -n perl-%{version}

%patch0 -p1

%build
/bin/sh Configure -des \
        -Doptimize="-g $RPM_OPT_FLAGS" \
        -Dlddlflags="-shared -g $RPM_OPT_FLAGS" \
        -Dmyhostname=build.openresty.org \
        -Dcc='ccache gcc' \
        -Dcf_by='orinc' \
        -Dinstallprefix=%{prefix} \
        -Dprefix=%{prefix} \
        -Darchname=%{_arch}-%{_os} \
        -Dvendorprefix=%{prefix} \
        -Dsiteprefix=%{prefix} \
        -Dprivlib="%{privlib}" \
        -Darchlib="%{archlib}" \
        -Duseshrplib \
        -Dusethreads \
        -Duseithreads \
        -Duselargefiles \
        -Dd_dosuid=n \
        -Dd_semctl_semun \
        -Di_shadow \
        -Di_syslog \
        -Dman3ext=3pm \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
        -Dpager='/usr/bin/less -isr' \
        -Dd_gethostent_r_proto -Ud_endhostent_r_proto -Ud_sethostent_r_proto \
        -Ud_endprotoent_r_proto -Ud_setprotoent_r_proto \
        -Ud_endservent_r_proto -Ud_setservent_r_proto \
        -Dscriptdir='%{prefix}/bin'

make -j`nproc`

%install
rm -rf %{buildroot}
make install.perl DESTDIR=%{buildroot}
rm -rf "%{buildroot}%{prefix}/lib/%{version}/pod/"

export QA_RPATHS=$(( 0x0020|0x0001|0x0010|0x0002 ))

#
# Core modules removal
#
# Dual-living binaries clashes on debuginfo files between perl and standalone
# packages. Excluding is not enough, we need to remove them. This is
# a work-around for rpmbuild bug #878863.
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -delete
# NB: fixed the permission for find-debuginfo.sh
chmod -R u+w $RPM_BUILD_ROOT/*
# remove all pod files
find $RPM_BUILD_ROOT -type f -name '*.pod' -delete
# trim POD code from all .pl or .pm files
# FirstTime.pm: special uses with pod, skip it.
find $RPM_BUILD_ROOT -type f \( -name '*.pm' -or -name '*.pl' \) \
    | grep -v 'FirstTime.pm' \
    | grep -v 'Opcode.pm' \
    | xargs -r sed -i -nE '/^=\w/,/^=cut/!p'

# tests -- FIXME need to validate that this all works as expected
mkdir -p %{buildroot}%{perl5_testdir}/perl-tests

%clean
rm -rf %{buildroot}

%files
# devel
%exclude %{prefix}/bin/h2xs
%exclude %{prefix}/bin/perlivp
%exclude %{archlib}/CORE/*.h

%attr(0755,root,root) %{prefix}/bin/
%{archlib}/
%{privlib}/

%files devel
%{prefix}/bin/h2xs
%{prefix}/bin/perlivp
%{archlib}/CORE/*.h

%changelog
* Sun Feb 7 2021 Jiahao Wang 5.24.4-1
- initial build for perl 5.24.4.
