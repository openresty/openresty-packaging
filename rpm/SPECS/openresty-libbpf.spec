Name:           openresty-libbpf
Version:        0.4.0.7
Release:        1%{?dist}
Summary:        OpenResty's fork of Libbpf

Group:          Development/Languages
License:        LGPLv2
URL:            https://openresty.com/
Source0:        libbpf-plus-%{version}.tar.gz
AutoReqProv:    no

%define _prefix     /usr/local/openresty-libbpf
%define elf_prefix  /usr/local/openresty-elfutils

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires: ccache, gcc, make, perl, pkgconfig
BuildRequires: openresty-elfutils-devel
Requires: openresty-elfutils

%description
Libbpf supports building BPF CO-RE-enabled applications, which,
in contrast to BCC, do not require Clang/LLVM runtime being deployed to
target servers and doesn't rely on kernel-devel headers being available.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/libbpf-plus-%{version}"; \
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
%setup -q -n libbpf-plus-%{version}

%build
cd src/ \
    && make -j`nproc` CC='ccache gcc -fdiagnostics-color=always' \
    CFLAGS='-I%{elf_prefix}/include -g3 -O3' \
    LDFLAGS='-L%{elf_prefix}/lib -Wl,-rpath,%{elf_prefix}/lib' \
    NO_PKG_CONFIG=1 \
    && cd ../

%install
cd src/ \
    && make install DESTDIR=%{buildroot} PREFIX=/usr/local/openresty-libbpf \
    LIBSUBDIR=lib \
    NO_PKG_CONFIG=1 \
    && cd ../

export QA_RPATHS=$(( 0x0020|0x0001|0x0010|0x0002 ))

%package devel
Summary: Openresty Shared Library for Libbpf
Requires: openresty-libbpf

%description devel
Openresty Shared Library for Libbpf

%files
%{_prefix}/lib/libbpf.so*

%files devel
%{_prefix}/lib/libbpf.a
%{_prefix}/lib/pkgconfig/*
%{_prefix}/include/*

%changelog
* Tue Jun 6 2023 Yichun Zhang (agentzh) 0.4.0.7-1
- upgraded libbpf-plus to 0.4.0.7.
* Sun Jun 4 2023 Yichun Zhang (agentzh) 0.4.0.6-1
- upgraded libbpf-plus to 0.4.0.6.
* Mon May 8 2023 Yichun Zhang (agentzh) 0.4.0.4-1
- upgraded libbpf-plus to 0.4.0.4.
* Mon May 8 2023 Yichun Zhang (agentzh) 0.4.0.3-1
- upgraded libbpf-plus to 0.4.0.3.
* Sun Jul 18 2021 Yichun Zhang (agentzh) 0.4.0.2-1
- upgraded libbpf-plus to 0.4.0.2.
* Mon Jun 21 2021 Yichun Zhang (agentzh) 0.4.0.1-1
- upgraded libbpf-plus to 0.4.0.1.
* Fri May 14 2021 Yichun Zhang (agentzh) 0.3.0.3-1
- upgraded libbpf-plus to 0.3.0.3.
* Fri May 14 2021 Jiahao Wang (johnny) 0.3.0.2-1
- upgraded libbpf-plus to 0.3.0.2.
* Thu May 06 2021 Jiahao Wang (johnny) 0.3.0.1-1
- initial packaging
