Name:           openresty-plus-hyperscan
Version:        5.0.0
Release:        2%{?dist}
Summary:        Hyperscan for OpenResty Plus

%define boost_version  1_69_0
%define boost_version2 1.69.0

License:        BSD
URL:            https://www.hyperscan.io
Source0:        https://github.com/intel/hyperscan/archive/v%{version}.tar.gz
Source1:        https://dl.bintray.com/boostorg/release/%{boost_version2}/source/boost_%{boost_version}.tar.bz2

Patch0:         hyperscan-g3-flag.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  pcre-devel
BuildRequires:  python

# we cannot specify the ragel dep for CentOS 6 does not have this package.
#BuildRequires:  ragel

BuildRequires:  sqlite-devel >= 3.0
BuildRequires:  gcc

Requires:       libstdc++

AutoReqProv:    no

#package requires SSE support and fails to build on non x86_64 archs
ExclusiveArch: x86_64

%define _missing_doc_files_terminate_build 0

%define hyperscan_prefix      /usr/local/openresty-plus/hyperscan

%description
Hyperscan for OpenResty Plus is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

%package devel
Summary: Libraries and header files for the hyperscan library of OpenResty Plus
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Hyperscan for OpenResty Plus is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

This package provides the libraries, include files and other resources
needed for developing Hyperscan applications.

%package runtime
Summary: Runtime for the hyperscan library of OpenResty Plus

%description runtime
Hyperscan for OpenResty Plus is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

This package provides the runtime for Hyperscan.

%prep
%setup -q -n hyperscan-%{version}
%patch0 -p1
%setup -D -T -a 1 -q -n hyperscan-%{version}

%build

ln -sf ../boost_%{boost_version}/boost include/boost

cmake -DCMAKE_INSTALL_PREFIX=%{hyperscan_prefix} -DBUILD_SHARED_LIBS=true .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/usr/local/openresty-plus/lualib/
ln -sf %{hyperscan_prefix}/%{_lib}/libhs.so %{buildroot}/usr/local/openresty-plus/lualib/
ln -sf %{hyperscan_prefix}/%{_lib}/libhs_runtime.so %{buildroot}/usr/local/openresty-plus/lualib/

mkdir -p %{buildroot}/usr/local/openresty-plus-debug/lualib/
ln -sf %{hyperscan_prefix}/%{_lib}/libhs.so %{buildroot}/usr/local/openresty-plus-debug/lualib/
ln -sf %{hyperscan_prefix}/%{_lib}/libhs_runtime.so %{buildroot}/usr/local/openresty-plus-debug/lualib/

rm -rf %{buildroot}%{hyperscan_prefix}/share/doc

%files
/usr/local/openresty-plus/lualib/libhs.so
/usr/local/openresty-plus-debug/lualib/libhs.so
%{hyperscan_prefix}/%{_lib}/*.so*
%exclude %{hyperscan_prefix}/%{_lib}/libhs_runtime.so*

%files devel
%{hyperscan_prefix}/include/hs/*
%{hyperscan_prefix}/%{_lib}/pkgconfig/libhs.pc

%files runtime
/usr/local/openresty-plus/lualib/libhs_runtime.so
/usr/local/openresty-plus-debug/lualib/libhs_runtime.so
%{hyperscan_prefix}/%{_lib}/libhs_runtime.so*

%changelog
* Sat Dec 22 2018 Ming Wen 5.0.0-1
- initial packaging.
