Summary:            Advanced IP routing and network device configuration tools
Name:               openresty-iproute2
Version:            6.3.0
Release:            1%{?dist}
Group:              Applications/System
URL:                http://kernel.org/pub/linux/utils/net/iproute2/
Source0:            http://kernel.org/pub/linux/utils/net/iproute2/iproute2-%{version}.tar.xz
AutoReqProv:        no

Patch0:             iproute2-with-libbpf.patch

%define _prefix         /usr/local/openresty-iproute2
%define libbpf_prefix   /usr/local/openresty-libbpf-net
%define libelf_prefix   /usr/local/openresty-elfutils

License:            GPLv2+ and Public Domain
BuildRequires:      bison, flex, libdb-devel, libmnl-devel, pkgconfig
BuildRequires:      ccache, patch
BuildRequires:      openresty-elfutils-devel
BuildRequires:      openresty-libbpf-net-devel
Requires:           libdb, libmnl
Requires:           openresty-elfutils
Requires:           openresty-libbpf-net

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
kernel.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/iproute2-%{version}"; \
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
%setup -q -n iproute2-%{version}
%patch0 -p1

%build
export PKG_CONFIG_PATH=%{libbpf_prefix}/lib/pkgconfig:%{libelf_prefix}/lib/pkgconfig
LIBBPF_FORCE=on \
    ./configure --prefix %{_prefix} --libbpf_dir=%{libbpf_prefix}
echo "" >> config.mk
echo "LDLIBS += -Wl,-rpath,%{libelf_prefix}/lib" >> config.mk
echo "CFLAGS += -g -O2" >> config.mk
make -j`nproc`

%install
make install DESTDIR=%{buildroot} \
    PREFIX=%{_prefix} \
    SBINDIR=%{_prefix}/sbin \
    CONFDIR=%{_prefix}/conf \
    ARPDDIR=%{_prefix}/arpd \
    HDRDIR=%{_prefix}/include/iproute2 \
    BASH_COMPDIR=%{_prefix}/bash_completion.d

# drop these files, iproute-doc package extracts files directly from _builddir
rm -rf '%{buildroot}%{_prefix}/share'

export QA_RPATHS=$(( 0x0020|0x0001|0x0010|0x0002 ))

%package devel
Summary: Openresty Shared Library for iproute2
Requires: openresty-iproute2

%description devel
Openresty Shared Library for iproute2

%files
%{_prefix}/sbin/*
%{_prefix}/bash_completion.d/*
%{_prefix}/conf/*
%{_prefix}/lib/tc/*.dist

%files devel
%{_prefix}/include/iproute2/*.h

%changelog
* Tue Jun 20 2023 Yichun Zhang (agentzh) 6.3.0-1
- upgraded iproute2 to 6.3.0.
* Tue Jun 13 2023 Yichun Zhang (agentzh) 5.17.0-1
- upgraded iproute2 to 5.17.0-1.
