Name:           openresty-symgen
Version:        0.0.4
Release:        1%{?dist}
Summary:        Tool for rebuilding symbol tables and debug info for ELF binary executables.

Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com

%define prefix          /usr/local/openresty-symgen
%define perlcc          /usr/local/openresty-perl/bin/perlcc

%define perl_ver            5.24.4
# NB: 5.24.4-4 is a version with the bugfix patch applied
%define perl_ver_rel        5.24.4-8
%define cpaneljsonxs_ver    4.28-2


Source0:        symgen-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

BuildRequires:  ccache, gcc, make
BuildRequires:  openresty-saas
BuildRequires:  openresty-perl >= %{perl_ver_rel}
BuildRequires:  openresty-perl-B-C >= 1.57-7
BuildRequires:  openresty-perl-Cpanel-JSON-XS >= %{cpaneljsonxs_ver}
BuildRequires:  openresty-perl-devel >= %{perl_ver_rel}

Requires:       openresty-saas
Requires:       openresty-utils
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
sed -i 's/\$FindBin::Bin/\/usr\/local\/openresty-symgen\/bin/' bin/*.pl
for f in `find bin -type f -name '*.lua'`; do
    /opt/openresty-saas/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm $f
done

make compile -j`nproc` PERLCC=%{perlcc}


%install
make install DESTDIR=%{buildroot} PREFIX=%{prefix}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{prefix}/bin/*.ljbc
%{prefix}/bin/asm2grams
%{prefix}/bin/cmp-grams
%{prefix}/bin/gen-auto-func-list
%{prefix}/bin/gen-func-json
%{prefix}/bin/gen-r2-af-cmds
%{prefix}/bin/rebuild-jl
%{prefix}/bin/gen-sym-ofs


%changelog
* Wed Dec 6 2023 Yichun Zhang (agentzh) 0.0.4-1
- upgraded openresty-symgen to 0.0.4.
* Fri Nov 3 2023 Yichun Zhang (agentzh) 0.0.3-1
- upgraded openresty-symgen to 0.0.3.
* Thu Sep 21 2023 Yichun Zhang (agentzh) 0.0.2-1
- upgraded openresty-symgen to 0.0.2.
* Tue Aug 29 2023 wanghuizzz <wanghui@openresty.com> - 0.0.1-1
- initial packaging
