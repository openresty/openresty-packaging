Name:           openresty-odb
Version:        0.20
Release:        2%{?dist}
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
make %{?_smp_mflags} \
    CXX='ccache g++ -fdiagnostics-color=always' \
    PCRE=%{pcre_prefix} \
    libodb-runtime.so

%install
make install DESTDIR=%{buildroot} PREFIX=%{prefix}

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%defattr(-,root,root,-)
%{prefix}/lib/libodb-runtime.so


%files devel
%defattr(-,root,root)
%{prefix}/include/odb-stat.h
%{prefix}/include/odb-runtime.h
%{prefix}/include/or-pcre.h
%{prefix}/include/or-utils.h


%changelog
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
