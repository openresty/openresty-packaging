Name:       openresty-edgcpfe
Version:    6.3.1.1
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
cp src/defines.h.linux src/defines.h \
    && cp sample_edg_eccp_config/edg_eccp_config.linux edg_eccp_config \
    && (cd lib && ../sample_edg_eccp_config/make_g++_incl_paths \
        && ../misc/make_predef_macro_table)
make -j"$(nproc)" CXX="ccache g++"
touch src/defines.h
make -j"$(nproc)" CXX="ccache g++" \
    CXXFLAGS='-DTARGET_YLANG=1 -std=gnu++11 -g -x c++'

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_prefix}/bin
install -m 0755 bin/edgcpfe %{buildroot}%{_prefix}/bin/edgcpfe
install -m 0755 bin/eccp %{buildroot}%{_prefix}/bin/eccp
install -m 0755 bin/edgcpdisp %{buildroot}%{_prefix}/bin/edgcpdisp

%files
%attr(0755,root,root) %{_prefix}/bin/edgcpfe
%attr(0755,root,root) %{_prefix}/bin/eccp
%attr(0755,root,root) %{_prefix}/bin/edgcpdisp

%clean
rm -rf %{buildroot}


%changelog
* Sun Feb 18 2024 Johnny Wang (jiahao) 6.3.1.1.
- initial package
