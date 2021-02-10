Name:           openresty-bcc
Version:        0.5.0
Release:        3%{?dist}
Summary:        BPF Compiler Collection (BCC)

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/iovisor/bcc
Source0:        https://github.com/iovisor/bcc/archive/v%{version}.tar.gz
AutoReqProv:    no

%define _prefix /usr/local/openresty-bcc
%define python_sitelib /lib/python2.7/site-packages

%if 0%{?fedora}
%define cmake cmake
%else
%define cmake cmake3
%endif

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

ExclusiveArch: x86_64 ppc64 aarch64 ppc64le
BuildRequires: bison %cmake flex make
BuildRequires: gcc gcc-c++ python2-devel elfutils-libelf-devel-static
BuildRequires: pkgconfig ncurses-devel openresty-clang-devel

%description
BCC is a toolkit for creating efficient kernel tracing and manipulation programs, and includes several useful tools and examples. It makes use of extended BPF (Berkeley Packet Filters), formally known as eBPF, a new feature that was first added to Linux 3.15. Much of what BCC uses requires Linux 4.1 and above.

%prep
%setup -q -n bcc-%{version}

%build
mkdir build
pushd build
%cmake .. -DREVISION_LAST=%{version} -DREVISION=%{version} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_PREFIX_PATH=/usr/local/openresty-clang/

make %{?_smp_mflags}
popd

%install
pushd build
make install DESTDIR=%{buildroot}

%package devel
Summary: Openresty Shared Library for BPF Compiler Collection (BCC)
Requires: elfutils-libelf

%description devel
Openresty Shared Library for BPF Compiler Collection (BCC)

%files devel
%{_prefix}/lib64/*
%{_prefix}/include/bcc/*
%exclude %{_prefix}/bin/
%exclude %{_prefix}/lib/
%exclude %{_prefix}/share/
