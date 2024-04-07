Name:       openresty-edgcpfe
Version:    6.6.0.11
Release:    1%{?dist}
Summary:    OpenResty's fork of EDG C++ Frontend Compiler
License:    Proprietary
Group:      Development/Languages
URL:        https://www.edg.com/

Source0:    edgcpfe-plus-%{version}.tar.gz

BuildRequires: ccache, gcc, gcc-c++

AutoReqProv: no

%define     _prefix /usr/local/openresty-edgcpfe

%description
OpenResty's fork of EDG C++ Frontend Compiler


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/edgcpfe-plus-%{version}"; \
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
%setup -q -n edgcpfe-plus-%{version}

%build
export EDG_BASE="%{buildroot}"
cp src/defines.h.linux src/defines.h
cp sample_edg_eccp_config/edg_eccp_config.linux edg_eccp_config
cd lib
../sample_edg_eccp_config/make_g++_incl_paths
../misc/make_predef_macro_table
cd ..
make -j"$(nproc)" CXX="ccache g++" \
    CXXFLAGS='-DTARGET_YLANG=1 -std=c++11 -g -x c++ -O2' LDFLAGS='-std=c++11'

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_prefix}/bin
install -m 0755 bin/y++ bin/edgcpfe bin/eccp bin/edgcpdisp %{buildroot}%{_prefix}/bin/
install -d %{buildroot}%{_prefix}/lib
install lib/* %{buildroot}%{_prefix}/lib/
install -d %{buildroot}%{_prefix}/include
install include/*.h include/*.stdh %{buildroot}%{_prefix}/include/

%files
%attr(0755,root,root) %{_prefix}/bin/edgcpfe
%attr(0755,root,root) %{_prefix}/bin/eccp
%attr(0755,root,root) %{_prefix}/bin/edgcpdisp
%attr(0755,root,root) %{_prefix}/bin/y++
%{_prefix}/lib/*
%attr(0644,root,root) %{_prefix}/include/*.h
%attr(0644,root,root) %{_prefix}/include/*.stdh

%clean
rm -rf %{buildroot}


%changelog
* Sat Apr 6 2024 Yichun Zhang (agentzh) 6.6.0.11-1
- upgraded openresty-edgcpfe to 6.6.0.11.
* Fri Mar 29 2024 Yichun Zhang (agentzh) 6.6.0.10-1
- upgraded openresty-edgcpfe to 6.6.0.10.
* Thu Mar 28 2024 Yichun Zhang (agentzh) 6.6.0.9-1
- upgraded openresty-edgcpfe to 6.6.0.9.
* Thu Mar 28 2024 Yichun Zhang (agentzh) 6.6.0.8-1
- upgraded openresty-edgcpfe to 6.6.0.8.
* Fri Feb 23 2024 Yichun Zhang (agentzh) 6.6.0.5-1
- upgraded openresty-edgcpfe to 6.6.0.5.
* Fri Feb 23 2024 Yichun Zhang (agentzh) 6.6.0.4-1
- upgraded openresty-edgcpfe to 6.6.0.4.
* Fri Feb 23 2024 Yichun Zhang (agentzh) 6.6.0.3-3
- added include/*.{h,stdh} files.
* Fri Feb 23 2024 Yichun Zhang (agentzh) 6.6.0.3-2
- added lib/* files.
* Fri Feb 23 2024 Yichun Zhang (agentzh) 6.6.0.3-1
- upgraded openresty-edgcpfe to 6.6.0.3.
* Fri Feb 23 2024 Yichun Zhang (agentzh) 6.6.0.2-1
- upgraded openresty-edgcpfe to 6.6.0.2.
* Fri Feb 23 2024 Yichun Zhang (agentzh) 6.6.0.1-1
- upgraded openresty-edgcpfe to 6.6.0.1.
* Sun Feb 18 2024 Johnny Wang (jiahao) 6.3.1.1.
- initial package
