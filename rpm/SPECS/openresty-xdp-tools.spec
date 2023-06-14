Name:           openresty-xdp-tools
Version:        1.2.2.1
Release:        1%{?dist}
Summary:        OpenResty's fork of xdp-tools

Group:          Development/Languages
License:        LGPLv2
URL:            https://openresty.com/
Source0:        xdp-tools-plus-%{version}.tar.gz
AutoReqProv:    no

%define _prefix         /usr/local/openresty-xdp-tools
%define libbpf_prefix   /usr/local/openresty-libbpf-net
%define libelf_prefix   /usr/local/openresty-elfutils
%define pcap_prefix     /usr/local/openresty-pcap
%define llvm_prefix     /usr/local/openresty-llvm

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires: ccache, gcc, make, perl, pkgconfig
BuildRequires: openresty-libbpf-net-devel
BuildRequires: openresty-pcap-devel >= 1.9.1-4
BuildRequires: openresty-elfutils-devel
BuildRequires: openresty-llvm
Requires: openresty-libbpf-net
Requires: openresty-pcap
Requires: openresty-elfutils

%description
Library and utilities for use with XDP

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/xdp-tools-plus-%{version}"; \
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
%setup -q -n xdp-tools-plus-%{version}

%build
export PKG_CONFIG_PATH=%{libbpf_prefix}/lib/pkgconfig:%{pcap_prefix}/lib/pkgconfig:%{libelf_prefix}/lib/pkgconfig
export LIBBPF_DIR=%{libbpf_prefix}
export LIBBPF_LIB_DIR=%{libbpf_prefix}/lib
export LIBBPF_INCLUDE_DIR=%{libbpf_prefix}/include
export PATH="%{llvm_prefix}/bin:$PATH"
CC="ccache gcc" CLANG="ccache %{llvm_prefix}/bin/clang" ./configure
echo "CFLAGS += -g -O2" >> config.mk
echo "LDFLAGS += -L%{pcap_prefix}/lib -L%{libelf_prefix}/lib" >> config.mk
echo "LDFLAGS += -Wl,-rpath,%{pcap_prefix}/lib:%{libelf_prefix}/lib:%{libbpf_prefix}/lib" >> config.mk
make -j`nproc`

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
# NB: these are object files, I deleted
rm -f %{buildroot}%{_prefix}/lib/bpf/*.o
rm -f %{buildroot}%{_prefix}/lib/libxdp.a
rm -rf %{buildroot}%{_prefix}/share/

export QA_RPATHS=$(( 0x0020|0x0001|0x0010|0x0002 ))

%package devel
Summary: Openresty Shared Library for xdp-tools
Requires: openresty-xdp-tools

%description devel
Openresty Shared Library for xdp-tools

%files
%{_prefix}/sbin/*
%{_prefix}/lib/libxdp.so*

%files devel
%{_prefix}/lib/pkgconfig/*
%{_prefix}/include/*

%changelog
* Tue Jun 13 2023 Jiahao Wang (wangjiahao) 1.2.2-1
- upgraded xdp-tools to 1.2.2-1.
