Name:           openresty-dw2c
Version:        2.06
Release:        1%{?dist}
Summary:        Tool for converting dwarf to C for OpenResty.

Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com

%define prefix          /usr/local/openresty-dw2c
%define perlcc          /usr/local/openresty-perl/bin/perlcc

%define perl_ver            5.24.4
# NB: 5.24.4-4 is a version with the bugfix patch applied
%define perl_ver_rel        5.24.4-8
%define cpaneljsonxs_ver    4.28-2


Source0:        dw2c-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

BuildRequires:  ccache, gcc, make, openresty-saas-pcre2-devel
BuildRequires:  openresty-yajl-devel >= 2.1.0.4
BuildRequires:  openresty-tcmalloc-devel
BuildRequires:  openresty-perl >= %{perl_ver_rel}
BuildRequires:  openresty-perl-B-C >= 1.57-7
BuildRequires:  openresty-perl-Cpanel-JSON-XS >= %{cpaneljsonxs_ver}
BuildRequires:  openresty-perl-devel >= %{perl_ver_rel}

Requires:       openresty-perl >= %{perl_ver_rel}
Requires:       openresty-perl-Cpanel-JSON-XS >= %{cpaneljsonxs_ver}
Requires:       openresty-tcmalloc, openresty-saas-pcre2
Requires:       openresty-yajl >= 2.1.0.4

%description
Tool for converting dwarf to C for OpenResty.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/dw2c-%{version}"; \
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
%setup -q -n dw2c-%{version}


%build
make compile USE_LTO=1 USE_TCM=1 -j2 PERLCC=%{perlcc} PREFIX=%{prefix}


%install
make install DESTDIR=%{buildroot} PREFIX=%{prefix}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/bin/dw2jl
%{prefix}/bin/dw2c++
%{prefix}/bin/dw2macros
%{prefix}/bin/dw2xml
%{prefix}/bin/find-altlink-files
%{prefix}/bin/gen-retaddrs


%changelog
* Wed Jun 5 2024 Yichun Zhang (agentzh) 2.06-1
- upgraded openresty-utils to 2.06.
* Wed Jun 5 2024 Yichun Zhang (agentzh) 2.05-1
- upgraded openresty-utils to 2.05.
* Wed Jun 5 2024 Yichun Zhang (agentzh) 2.04-1
- upgraded openresty-utils to 2.04.
* Tue Apr 16 2024 Yichun Zhang (agentzh) 2.03-1
- upgraded openresty-utils to 2.03.
* Tue Dec 5 2023 Yichun Zhang (agentzh) 2.02-1
- upgraded openresty-utils to 2.02.
* Thu Nov 9 2023 Yichun Zhang (agentzh) 2.01-1
- upgraded openresty-utils to 2.01.
* Wed Nov 8 2023 Yichun Zhang (agentzh) 1.10-1
- upgraded openresty-utils to 1.10.
* Mon Oct 16 2023 Yichun Zhang (agentzh) 1.8-1
- upgraded openresty-utils to 1.8.
* Wed Oct 11 2023 Yichun Zhang (agentzh) 1.7-1
- upgraded openresty-utils to 1.7.
* Tue Sep 19 2023 Yichun Zhang (agentzh) 1.6-1
- upgraded openresty-utils to 1.6.
* Tue Sep 12 2023 Yichun Zhang (agentzh) 1.5-1
- upgraded openresty-utils to 1.5.
* Wed Jul 26 2023 Yichun Zhang (agentzh) 1.4-1
- upgraded openresty-utils to 1.4.
* Wed Jul 26 2023 Yichun Zhang (agentzh) 1.3-1
- upgraded openresty-utils to 1.3.
* Thu Jun 8 2023 Yichun Zhang (agentzh) 1.2-1
- upgraded openresty-utils to 1.2.
* Tue May 23 2023 Yichun Zhang (agentzh) 1.1-1
- upgraded openresty-utils to 1.1.
* Fri Apr 21 2023 Yichun Zhang (agentzh) 1.0-1
- upgraded openresty-utils to 1.0.
* Wed Apr 5 2023 Yichun Zhang (agentzh) 0.9-1
- upgraded openresty-utils to 0.9.
* Mon Mar 6 2023 Yichun Zhang (agentzh) 0.7-1
- upgraded openresty-utils to 0.7.
* Sun Oct 30 2022 Yichun Zhang (agentzh) 0.6-1
- upgraded openresty-utils to 0.6.
* Mon Oct 10 2022 Yichun Zhang (agentzh) 0.5-1
- upgraded openresty-utils to 0.5.
* Sun Oct 2 2022 Yichun Zhang (agentzh) 0.4-1
- upgraded openresty-utils to 0.4.
* Thu Aug 25 2022 Yichun Zhang (agentzh) 0.3-1
- upgraded openresty-utils to 0.3.
* Sun May 8 2022 Yichun Zhang (agentzh) 0.2-1
- upgraded openresty-utils to 0.2.
* Thu May 05 2022 Johnny Wang <wangjiahao@openresty.com> - 0.1-1
- initial packaging
