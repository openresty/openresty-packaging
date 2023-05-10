Name:           openresty-ebpf-plus
Version:        0.0.1
Release:        1%{?dist}
Summary:        OpenResty's fork of ebpf

Group:          Development/Languages
License:        LGPLv2
URL:            https://openresty.com/
Source0:        ebpf-plus-%{version}.tar.gz
AutoReqProv:    no

%define _prefix     /usr/local/openresty-ebpf-plus

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%description
eBPF is part of the mainline kernel so it will have a larger user base than
SystemTap and will also get more attention (bug fixes and enhancements) from
the kernel developers over the years. SystemTap is an out-of-tree project and
will remain so.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/ebpf-plus-%{version}"; \
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
%setup -q -n ebpf-plus-%{version}

%install
install -d %{buildroot}%{_prefix}/include/
install -m 0644 include/*.h %{buildroot}%{_prefix}/include/

export QA_RPATHS=$(( 0x0020|0x0001|0x0010|0x0002 ))

%files
%{_prefix}/include/*

%changelog
* Wed May 10 2023 Yichun Zhang (agentzh) 0.0.1-1
- upgraded ebpf-plus to 0.0.1-1.
