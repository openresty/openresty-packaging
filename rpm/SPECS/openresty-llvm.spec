Name:               openresty-llvm
Version:            14.0.0.1
Release:            3%{?dist}
Summary:            OpenResty Inc's proprietary LLVM fork

Group:              System Environment/Libraries

License:            Apache License 2.0
URL:                https://github.com/orinc/llvm-plus/
Source0:            llvm-plus-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	ccache
BuildRequires:	cmake
#BuildRequires:	ninja-build
BuildRequires:	zlib-devel
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
%if %{with gold}
BuildRequires:	binutils-devel
%endif
# LLVM's LineEditor library will use libedit if it is available.
#BuildRequires:	libedit-devel

#https://src.fedoraproject.org/rpms/llvm/blob/f36/f/llvm.spec#_204
#BuildRequires:	python3-psutil
#BuildRequires:	python3-sphinx
#BuildRequires:	python3-recommonmark
# We need python3-devel for %%py3_shebang_fix
#BuildRequires:	python3-devel
#BuildRequires:	python3-setuptools

AutoReqProv:        no

%undefine __brp_mangle_shebangs
%define llvm_prefix     /usr/local/openresty-llvm


%description
OpenResty Inc's proprietary LLVM fork

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/llvm-plus-%{version}"; \
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
%setup -q -n llvm-plus-%{version}


%build
mkdir build
cd build/
cmake -DLLVM_LINK_LLVM_DYLIB=ON -DLLVM_BUILD_LLVM_DYLIB=ON \
    -DLLVM_TARGETS_TO_BUILD="WebAssembly;X86;BPF" -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_PROJECTS="lld;clang;compiler-rt" \
    -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
    -DLLVM_INCLUDE_TESTS=OFF \
    -DLLVM_INCLUDE_GO_TESTS=OFF \
    -DLLVM_INCLUDE_BENCHMARKS=OFF \
    -DCMAKE_INSTALL_PREFIX=%{llvm_prefix} ../llvm
find . -name flags.make | xargs sed -i 's/ -g / /g'

free=`free -m|grep -E '^Mem'|head -n2|awk '{print $NF}'`
ncpus=`nproc`
max_jobs=$(( $free / 1100 ))
#echo "max jobs: $max_jobs"
if [ "$max_jobs" -gt "$ncpus" ]; then
    max_jobs=$ncpus
fi
#echo "max jobs: $max_jobs"
make -j$max_jobs

%install
cd build/
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{llvm_prefix}/man
find %{buildroot}/%{llvm_prefix} -name "*.a" -delete


%clean
rm -rf %{buildroot}


%files
%{llvm_prefix}/bin/
%{llvm_prefix}/lib/
%{llvm_prefix}/libexec/
%{llvm_prefix}/share/
%{llvm_prefix}/include/


%changelog
* Mon Apr 17 2023 Yichun Zhang (agentzh) 14.0.0.1

- upgraded llvm-plus to 14.0.0.1
