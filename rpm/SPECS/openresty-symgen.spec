Name:           openresty-symgen
Version:        0.1.1
Release:        1%{?dist}
Summary:        Tool for rebuilding symbol tables and debug info for ELF binary executables.

Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com

%define prefix          /usr/local/openresty-symgen
%define perl_bin        /usr/local/openresty-perl/bin
%define perlcc          %{perl_bin}/perlcc

%define perl_ver            5.24.4
# NB: 5.24.4-4 is a version with the bugfix patch applied
%define perl_ver_rel        5.24.4-8
%define cpaneljsonxs_ver    4.28-2


Source0:        symgen-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

BuildRequires:  ccache, gcc, make
BuildRequires:  openresty-saas, openresty-radare2-devel >= 5.0.3.3
BuildRequires:  openresty-perl >= %{perl_ver_rel}
BuildRequires:  openresty-perl-B-C >= 1.57-7
BuildRequires:  openresty-perl-Cpanel-JSON-XS >= %{cpaneljsonxs_ver}
BuildRequires:  openresty-perl-devel >= %{perl_ver_rel}

Requires:       openresty-saas
Requires:       openresty-utils, openresty-radare2 >= 5.0.3.3
Requires:       openresty-perl >= %{perl_ver_rel}
Requires:       openresty-perl-Cpanel-JSON-XS >= %{cpaneljsonxs_ver}

%description
Tool for converting dwarf to C for OpenResty.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/symgen-%{version}"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%endif

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%if 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%prep
%setup -q -n symgen-%{version}

%build
#sed -i 's/^use  *lib\>/use lib "\/usr\/local\/openresty-symgen\/lib", /' bin/*.pl
sed -i 's/\t\(bin\/symgen-src-filter.pl -o\)/\tperl -Ilib \1/g' Makefile

for i in 1 2 3; do
    PATH=%{perl_bin}:$PATH make compile -j`nproc` PERLCC=%{perlcc} && break
done

%install
make install DESTDIR=%{buildroot} PREFIX=%{prefix}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{prefix}/bin/asm2grams
%{prefix}/bin/cmp-grams
%{prefix}/bin/gen-func-json
%{prefix}/bin/gen-r2-af-cmds
%{prefix}/bin/rebuild-jl
%{prefix}/bin/gen-sym-ofs
%{prefix}/bin/func-retval


%changelog
* Sun Feb 4 2024 Yichun Zhang (agentzh) 0.1.1-1
- upgraded openresty-symgen to 0.1.1.
* Sun Dec 10 2023 Yichun Zhang (agentzh) 0.0.9-1
- upgraded openresty-symgen to 0.0.9.
* Fri Dec 8 2023 Yichun Zhang (agentzh) 0.0.8-1
- upgraded openresty-symgen to 0.0.8.
* Fri Dec 8 2023 Yichun Zhang (agentzh) 0.0.7-1
- upgraded openresty-symgen to 0.0.7.
* Wed Dec 6 2023 Yichun Zhang (agentzh) 0.0.6-1
- upgraded openresty-symgen to 0.0.6.
* Wed Dec 6 2023 Yichun Zhang (agentzh) 0.0.5-1
- upgraded openresty-symgen to 0.0.5.
* Wed Dec 6 2023 Yichun Zhang (agentzh) 0.0.4-1
- upgraded openresty-symgen to 0.0.4.
* Fri Nov 3 2023 Yichun Zhang (agentzh) 0.0.3-1
- upgraded openresty-symgen to 0.0.3.
* Thu Sep 21 2023 Yichun Zhang (agentzh) 0.0.2-1
- upgraded openresty-symgen to 0.0.2.
* Tue Aug 29 2023 wanghuizzz <wanghui@openresty.com> - 0.0.1-1
- initial packaging
