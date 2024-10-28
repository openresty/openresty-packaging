Name:               openresty-elf-loader
Version:            0.0.5
Release:            1%{?dist}
Summary:            The elf-loader library for OpenResty

Group:              System Environment/Libraries

License:            Proprietary
URL:                https://github.com/orinc/elf-loader
Source0:            elf-loader-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      openresty-elfutils-devel

AutoReqProv:        no

%define elf_loader_prefix     /usr/local/elf-loader


%description
The elf loader compression library for use by OpenResty ONLY

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/elf-loader-%{version}"; \
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


%package devel

Summary:            Development files for OpenResty's elf loader library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty's elf loader library.


%prep
%setup -q -n elf-loader-%{version}


%build
make -j`nproc`


%install
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{elf_loader_prefix}/lib/liborelfloader.so*


%files devel
%defattr(-,root,root,-)

%{elf_loader_prefix}/include/*.h


%changelog
* Mon Oct 28 2024 Yichun Zhang (agentzh) 0.0.5-1
- upgraded elf-loader to 0.0.5.
* Sat Mar 23 2024 Yichun Zhang (agentzh) 0.0.3-1
- upgraded elf-loader to 0.0.3.
* Thu Mar 10 2022 Yichun Zhang (agentzh) 0.0.2-1
- upgraded elf-loader to 0.0.2.
* Mon Feb 07 2022 Yichun Zhang 0.0.1
- initial version
