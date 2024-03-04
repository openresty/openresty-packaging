Name:           openresty-absl
Version:        20240116.1
Release:        1%{?dist}
Summary:        OpenResty's fork of abseil.
Group:          Development/Tools
License:        Apache License 2.0
URL:            https://abseil.io/

Source0:        https://github.com/abseil/abseil-cpp/archive/refs/tags/%{version}.tar.gz

%if 0%{?fedora}
%define cmake cmake
%else
%define cmake cmake3
%endif

BuildRequires: ccache, gcc, gcc-c++
BuildRequires: make
BuildRequires: %cmake

AutoReqProv: no

%global debug_package %{nil}
%global __spec_install_post %{nil}
%define prefix %{_usr}/local/%{name}

%description
OpenResty's fork of abseil.
Abseil is an open source collection of C++ libraries drawn from the most
fundamental pieces of Google’s internal codebase. These libraries are the
nuts-and-bolts that underpin almost everything Google runs.

%package    devel
Summary:    openresty-absl for devel

%description devel
openresty-absl for devel

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/abseil-cpp-%{version}"; \
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
%setup -q -n abseil-cpp-%{version}


%build
mkdir build
cd build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{prefix}/lib -DCMAKE_INSTALL_PREFIX=%{prefix} \
    -DABSL_BUILD_TESTING=OFF -DABSL_USE_GOOGLETEST_HEAD=OFF \
    -DCMAKE_CXX_COMPILER_LAUNCHER='ccache' \
    -DCMAKE_CXX_FLAGS="-O2 -g" \
    ..
make -j$(nproc)

%install
cd build
make install DESTDIR=%{buildroot}

export QA_RPATHS=$[ 0x0012 ]

%clean
rm -rf %{buildroot}

%files
%dir %{prefix}

%files devel
%{prefix}/lib/*
%{prefix}/include/*

%changelog
* Mon Mar 04 2024 Jiahao Wang <wangjiahao@openresty.com>
- initial packaging
