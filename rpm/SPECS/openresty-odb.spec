Name:           openresty-odb
Version:        0.40
Release:        1%{?dist}
Summary:        OpenResty Debugger based on ptrace
Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com/
Provides:       openresty-odb

Source0:        odb-%{version}.tar.gz

AutoReqProv:    no

#%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%define prefix /usr/local/openresty-odb
%define pcre_prefix /opt/openresty-saas/pcre


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ccache, gcc-c++
BuildRequires: openresty-saas-pcre-devel
Requires: openresty-saas-pcre

%description
OpenResty Debugger based on ptrace


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/odb-%{version}"; \
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


# ------------------------------------------------------------------------

%package devel
Summary:            Development files for %{name} SaaS
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Development files for OpenResty Debugger based on ptrace.


%prep
%setup -q -n odb-%{version}


%build
make -j`nproc` \
    CXX='ccache g++ -fdiagnostics-color=always' \
    PCRE=%{pcre_prefix} \
    libodb-runtime.so

%install
make install DESTDIR=%{buildroot} PREFIX=%{prefix} \
    CXX='ccache g++ -fdiagnostics-color=always' \
    PCRE=%{pcre_prefix} \

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%dir %{prefix}
%dir %{prefix}/lib
%defattr(-,root,root,-)
%{prefix}/lib/libodb-runtime.so


%files devel
%defattr(-,root,root)
%dir %{prefix}/include
%{prefix}/include/odb-stat.h
%{prefix}/include/odb-runtime.h
%{prefix}/include/odb-runtime-config.h
%{prefix}/include/or-pcre.h
%{prefix}/include/or-utils.h


%changelog
* Wed Sep 11 2024 Yichun Zhang (agentzh) 0.40-1
- upgraded odb to 0.40.
* Tue Apr 16 2024 Yichun Zhang (agentzh) 0.39-1
- upgraded odb to 0.39.
* Mon Mar 4 2024 Yichun Zhang (agentzh) 0.38-1
- upgraded odb to 0.38.
* Sun Dec 10 2023 Yichun Zhang (agentzh) 0.37-1
- upgraded odb to 0.37.
* Fri Dec 1 2023 Yichun Zhang (agentzh) 0.36-1
- upgraded odb to 0.36.
* Sun Jan 29 2023 Yichun Zhang (agentzh) 0.35-1
- upgraded odb to 0.35.
* Mon Oct 24 2022 Yichun Zhang (agentzh) 0.34-1
- upgraded odb to 0.34.
* Tue Aug 2 2022 Yichun Zhang (agentzh) 0.33-1
- upgraded odb to 0.33.
* Tue Jun 21 2022 Yichun Zhang (agentzh) 0.32-1
- upgraded odb to 0.32.
* Thu Jun 16 2022 Yichun Zhang (agentzh) 0.31-1
- upgraded odb to 0.31.
* Mon Nov 1 2021 Yichun Zhang (agentzh) 0.30-1
- upgraded odb to 0.30.
* Wed Jul 28 2021 Yichun Zhang (agentzh) 0.29-1
- upgraded odb to 0.29.
* Sun Jul 25 2021 Yichun Zhang (agentzh) 0.28-1
- upgraded odb to 0.28.
* Sun Jul 25 2021 Yichun Zhang (agentzh) 0.27-1
- upgraded odb to 0.27.
* Tue Jul 6 2021 Yichun Zhang (agentzh) 0.26-1
- upgraded odb to 0.26.
* Mon May 10 2021 Yichun Zhang (agentzh) 0.25-1
- upgraded odb to 0.25.
* Thu Mar 25 2021 Yichun Zhang (agentzh) 0.24-1
- upgraded odb to 0.24.
* Wed Feb 3 2021 Yichun Zhang (agentzh) 0.23-1
- upgraded odb to 0.23.
* Mon Jan 18 2021 Yichun Zhang (agentzh) 0.22-1
- upgraded odb to 0.22.
* Sun Jan 10 2021 Yichun Zhang (agentzh) 0.21-1
- upgraded odb to 0.21.
* Wed Nov 4 2020 Yichun Zhang (agentzh) 0.20-1
- upgraded odb to 0.20.
* Tue Nov 3 2020 Yichun Zhang (agentzh) 0.19-1
- upgraded odb to 0.19.
* Thu Aug 20 2020 Yichun Zhang (agentzh) 0.18-1
- upgraded odb to 0.18.
* Thu Jul 23 2020 Yichun Zhang (agentzh) 0.17-1
- upgraded odb to 0.17.
* Thu Jul 23 2020 Yichun Zhang (agentzh) 0.16-1
- upgraded odb to 0.16.
* Wed Jun 24 2020 Yichun Zhang (agentzh) 0.15-1
- upgraded odb to 0.15.
* Tue Jun 23 2020 Yichun Zhang (agentzh) 0.14-1
- upgraded odb to 0.14.
* Tue Jun 23 2020 Yichun Zhang (agentzh) 0.13-1
- upgraded odb to 0.13.
* Mon Jun 22 2020 Yichun Zhang (agentzh) 0.12-1
- upgraded odb to 0.12.
* Mon Jun 22 2020 Yichun Zhang (agentzh) 0.11-1
- upgraded odb to 0.11.
* Mon Jun 22 2020 Yichun Zhang (agentzh) 0.10-1
- upgraded odb to 0.10.
* Sun Jun 21 2020 Yichun Zhang (agentzh) 0.09-1
- upgraded odb to 0.09.
* Sun Jun 21 2020 Yichun Zhang (agentzh) 0.08-1
- upgraded odb to 0.08.
* Sun Jun 14 2020 Yichun Zhang (agentzh) 0.06-1
- upgraded odb to 0.06.
* Mon Jun 8 2020 Yichun Zhang (agentzh) 0.05-1
- upgraded odb to 0.05.
* Mon Jun 8 2020 Jiahao Wang 0.04-1
- upgraded odb to 0.04-1.
* Sun Jun 7 2020 Jiahao Wang 0.03-1
- upgraded odb to 0.03-1.
* Sun Jun 7 2020 Jiahao Wang 0.02-1
- initial build for odb 0.02-1.
