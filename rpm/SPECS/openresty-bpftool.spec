%define pkgname bpftool-plus

Name:           openresty-bpftool
Version:        5.13.18.8
Release:        2%{?dist}
Summary:        OpenResty's fork of bpftool

Group:          Development/Languages
License:        LGPLv2
URL:            https://openresty.com/
Source0:        %{pkgname}-%{version}.tar.gz
AutoReqProv:    no

%define _prefix         /usr/local/openresty-bpftool
%define libbpf_prefix   /usr/local/openresty-libbpf
%define elf_prefix      /usr/local/openresty-elfutils
%define binutils_prefix /usr/local/openresty-binutils
%define or_zlib_prefix  /opt/openresty-saas/zlib

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

# vim provides the xxd tool needed by the build system.
BuildRequires: ccache, gcc, make, perl, pkgconfig, vim
BuildRequires: openresty-libbpf-devel >= 0.4.0.8-1
BuildRequires: openresty-elfutils-devel
BuildRequires: openresty-binutils-devel >= 2.39.0.2-2
BuildRequires: openresty-saas-zlib-devel
BuildRequires: libcap-devel
Requires: openresty-libbpf >= 0.4.0.8-1
Requires: openresty-elfutils
Requires: openresty-binutils >= 2.39.0.2-2
Requires: openresty-saas-zlib
Requires: libcap

%description
OpenResty Inc's private fork of bpftool from the Linux kernel.


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
    -lbpf -lz -lcap -lbfd -ldl -lelf -lopcodes'

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

export QA_RPATHS=$(( 0x0020|0x0001|0x0010|0x0002 ))

%files
%{_prefix}/bin/bpftool

%changelog
* Wed Feb 14 2024 Yichun Zhang (agentzh) 5.13.18.8-2
- upgraded bpftool-plus to 5.13.18.8.
* Thu Jun 29 2023 Yichun Zhang (agentzh) 5.13.18.8-1
- upgraded bpftool-plus to 5.13.18.8.
* Tue Jun 6 2023 Yichun Zhang (agentzh) 5.13.18.7-1
- upgraded bpftool-plus to 5.13.18.7.
* Sun Jun 4 2023 Yichun Zhang (agentzh) 5.13.18.6-1
- upgraded bpftool-plus to 5.13.18.6.
* Sun May 14 2023 Yichun Zhang (agentzh) 5.13.18.5-1
- upgraded bpftool-plus to 5.13.18.5.
* Thu May 11 2023 Yichun Zhang (agentzh) 5.13.18.4-1
- upgraded bpftool-plus to 5.13.18.4.
* Wed May 10 2023 Yichun Zhang (agentzh) 5.13.18.3-1
- upgraded bpftool to 5.13.18.3
* Tue May 9 2023 Yichun Zhang (agentzh) 5.13.18.2-1
- upgraded bpftool to 5.13.18.2
