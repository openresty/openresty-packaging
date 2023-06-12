%define pkgname bpftool-plus

Name:           openresty-bpftool-net
Version:        5.13.18.7
Release:        1%{?dist}
Summary:        OpenResty's fork of bpftool (networking)

Group:          Development/Languages
License:        LGPLv2
URL:            https://openresty.com/
Source0:        %{pkgname}-%{version}.tar.gz
AutoReqProv:    no

%define _prefix         /usr/local/openresty-bpftool-net
%define libbpf_prefix   /usr/local/openresty-libbpf-net
%define elf_prefix      /usr/local/openresty-elfutils
%define binutils_prefix /usr/local/openresty-binutils
%define or_zlib_prefix  /usr/local/openresty/zlib

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

# vim provides the xxd tool needed by the build system.
BuildRequires: ccache, gcc, make, perl, pkgconfig, vim
BuildRequires: openresty-libbpf-net-devel >= 0.4.0.8-2
BuildRequires: openresty-elfutils-devel
BuildRequires: openresty-binutils-devel >= 2.39.0.2-2
BuildRequires: openresty-zlib-devel
BuildRequires: libcap-devel
Requires: openresty-libbpf-net >= 0.4.0.8-2
Requires: openresty-elfutils
Requires: openresty-binutils >= 2.39.0.2-2
Requires: openresty-zlib
Requires: libcap

%description
OpenResty Inc's private fork of bpftool from the Linux kernel (networking).


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{pkgname}-%{version}"; \
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


%clean
rm -rf %{buildroot}


%prep
%setup -q -n %{pkgname}-%{version}

%build
make LIBBPF_PREFIX=%{libbpf_prefix} BINUTILS_PREFIX=%{binutils_prefix} \
    LIBZ_PREFIX=%{or_zlib_prefix} \
    CC='ccache gcc -fdiagnostics-color=always -g' \
    LDFLAGS='-L%{libbpf_prefix}/lib -L%{elf_prefix}/lib -L%{binutils_prefix}/lib \
	-L%{or_zlib_prefix}/lib \
    -Wl,-rpath,%{libbpf_prefix}/lib:%{elf_prefix}/lib:%{binutils_prefix}/lib:%{or_zlib_prefix}/lib \
    -lbpf -lz -lcap -lbfd -ldl -lelf -lopcodes' NET=1

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot} NET=1

export QA_RPATHS=$(( 0x0020|0x0001|0x0010|0x0002 ))

%files
%{_prefix}/bin/bpftool

%changelog
* Mon Jun 12 2023 Yichun Zhang (agentzh) 5.13.18.7-1
- initial packaging.
