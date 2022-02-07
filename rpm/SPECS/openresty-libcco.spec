Name:               openresty-libcco
Version:            0.0.1
Release:            1%{?dist}
Summary:            The high performance c-coherent library for OpenResty

Group:              System Environment/Libraries

License:            Proprietary
URL:                https://github.com/orinc/libcco
Source0:            libcco-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:

AutoReqProv:        no

%define libcco_prefix     /usr/local/libcco


%description
The library aims to provide a high performance c-coherent library, compatible with ucontext API.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/libcco-%{version}"; \
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

Summary:            Development files for OpenResty's libcco library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty's libcco library.


%prep
%setup -q -n libcco-%{version}


%build
make -j`nproc`  OPTIMIZES=""


%install
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{libcco_prefix}/lib/libcco.so*


%files devel
%defattr(-,root,root,-)

%{libcco_prefix}/include/libcco.h


%changelog
* Mon Feb 07 2022 Yichun Zhang 0.0.1
- initial version
