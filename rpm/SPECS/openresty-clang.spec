Name:           openresty-clang
Version:        5.0.0
Release:        1%{?dist}
Summary:        llvm + clang used only for bpf program

License:        NCSA
URL:            http://llvm.org
Source0:        http://llvm.org/releases/%{version}/llvm-%{version}.src.tar.xz
Source1:        http://llvm.org/releases/%{version}/cfe-%{version}.src.tar.xz

%define _prefix /usr/local/openresty-clang

%define debug_package %{nil}

%if 0%{?fedora}
%define cmake cmake
%else
%define cmake cmake3
%endif

BuildRequires: %cmake
BuildRequires: libffi-devel
BuildRequires: ncurses-devel
BuildRequires: multilib-rpm-config
BuildRequires: binutils-devel
BuildRequires: gcc gcc-c++

%description
LLVM is a compiler infrastructure designed for compile-time, link-time,
runtime, and idle-time optimization of programs from arbitrary programming
languages. The compiler infrastructure includes mirror sets of programming
tools as well as libraries with equivalent functionality.

%prep
%setup -q -c -b 1
mv ../cfe-%{version}.src llvm-%{version}.src/tools/clang

%build
mkdir -p build
cd build

%cmake ../llvm-%{version}.src -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX='%{_prefix}' \
    -DLLVM_TARGETS_TO_BUILD=X86\;BPF  \
    -DLLVM_LIBDIR_SUFFIX=64 \
    -DLLVM_INSTALL_BINUTILS_SYMLINKS=OFF \
    -DLLVM_INCLUDE_EXAMPLES=OFF \
    -DLLVM_INCLUDE_TESTS=OFF \
    -DLLVM_ENABLE_DIA_SDK=OFF \
    -DLLVM_BUILD_DOCS=OFF \
    -DSPHINX_WARNINGS_AS_ERRORS=OFF \
    -DLLVM_BUILD_INSTRUMENTED_COVERAGE=OFF

make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

%package devel
Summary: clang and llvm for devel

%description devel
clang and llvm for devel

%files devel
%{_prefix}/include/*
%{_prefix}/lib64/*
%{_prefix}/bin/*
%exclude %{_prefix}/libexec/
%exclude %{_prefix}/share/
