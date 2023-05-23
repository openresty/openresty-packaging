Name:           openresty-orbpf-ko
Version:        0.0.1
Release:        1%{?dist}
Summary:        BPF kernel module implemented by OpenResty INC.

Group:          Development/Languages
License:        LGPLv2
URL:            https://openresty.com/
Source0:        orbpf-ko-%{version}.tar.gz
AutoReqProv:    no
BuildArch:      noarch

%define _prefix     /usr/local/openresty-orbpf-ko

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%description
BPF kernel module implemented by OpenResty INC.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/orbpf-ko-%{version}"; \
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
%setup -q -n orbpf-ko-%{version}

%install
install -d %{buildroot}%{_prefix}/src/
install -d %{buildroot}%{_prefix}/src/auto
install -m 0644 *.h *.c *.S Makefile %{buildroot}%{_prefix}/src/
install -m 0644 auto/*.c %{buildroot}%{_prefix}/src/auto/

%files
%{_prefix}/src/*.c
%{_prefix}/src/*.h
%{_prefix}/src/*.S
%{_prefix}/src/Makefile
%{_prefix}/src/auto/*.c

%changelog
* Tue May 23 2023 Yichun Zhang (agentzh) 0.0.1-1
- upgraded orbpf-ko to 0.0.1-1.
