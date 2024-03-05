Name:           openresty-gdb-runtime
Version:        0.0.3
Release:        1%{?dist}
Summary:        OpenResty GDB Runtime Library
Group:          Development/Libraries
License:        Proprietary
URL:            https://openresty.com/
Source0:        gdb-runtime-%{version}.tar.gz

AutoReqProv: no

%define prefix /usr/local/openresty-gdb-runtime
%define pcre_prefix /opt/openresty-saas/pcre

%define debug_package %{nil}

BuildRequires:  gcc-c++
BuildRequires: openresty-saas-pcre-devel
Requires: openresty-saas-pcre


%description
OpenResty GDB Runtime Library.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/gdb-runtime-%{version}"; \
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
%setup -q -n gdb-runtime-%{version}


%build
make -j`nproc` \
    PREFIX=%{prefix} \
    PCRE=%{pcre_prefix} \
    CXX='g++ -fdiagnostics-color=always'


%install
make install \
    DESTDIR=%{buildroot} \
    PREFIX=%{prefix} \
    PCRE=%{pcre_prefix}


%files
%defattr(-, root, root)
%dir %{prefix}
%dir %{prefix}/objs
%dir %{prefix}/include
%defattr(-,root,root,-)
%{prefix}/include/*.h
%{prefix}/objs/*.o


%clean
rm -rf %{buildroot}


%changelog
* Mon Mar 4 2024 Yichun Zhang (agentzh) 0.0.3-1
- upgraded openresty-gdb-runtime to 0.0.3.
* Mon Mar 4 2024 Yichun Zhang (agentzh) 0.0.2-1
- upgraded openresty-gdb-runtime to 0.0.2.
* Fri Mar 1 2024 wanghuizzz 0.0.1
- initial build for openresty-gdb-runtime 0.0.1.
