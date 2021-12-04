Name:               openresty-boringssl
Version:            20211122
Release:            2%{?dist}
Summary:            BoringSSL library for OpenResty

Group:              Development/Libraries

# https://github.com/google/boringssl/blob/master/LICENSE
License:            OpenSSL + ISC
URL:                https://boringssl.googlesource.com/boringssl
Source0:            boringssl-plus-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# CMake 3.5 or later is required.
# A recent version of Perl is required.
# C and C++ compilers with C++11 support are required. GCC7 or above
# The most recent stable version of Go is required.
BuildRequires:      gcc, make, gcc-c++, libunwind
BuildRequires:      openresty-zlib-devel >= 1.2.11
Requires:           openresty-zlib >= 1.2.11

AutoReqProv:        no

%define openssl_prefix      /usr/local/openresty/boringssl
%define zlib_prefix         /usr/local/openresty/zlib


%description
This boringssl library build is specifically for OpenResty uses. It may contain
custom patches from OpenResty.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/boringssl-plus-%{version}"; \
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

Summary:            Development files for OpenResty's OpenSSL library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
Provides C header and static library for OpenResty's OpenSSL library.


%prep
%setup -q -n boringssl-plus-%{version}



%build
export PATH=/opt/go/bin:$PATH
mkdir -p build
cd build
cmake -DCMAKE_VERBOSE_MAKEFILE=ON -DBUILD_SHARED_LIBS=1 \
      -DCMAKE_CXX_FLAGS="-Og -g -I%{zlib_prefix}/include" \
      -DCMAKE_C_FLAGS="-Og -g -I%{zlib_prefix}/include" \
      -DCMAKE_SHARED_LINKER_FLAGS="-L%{zlib_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib" \
      -DCMAKE_BUILD_TYPE=Release ..

make -j`nproc` ssl crypto

%install
install -d %{buildroot}%{openssl_prefix}/lib
install -d %{buildroot}%{openssl_prefix}/include/openssl
install -m 0755 ./build/crypto/libcrypto.so.* %{buildroot}%{openssl_prefix}/lib
(cd %{buildroot}%{openssl_prefix}/lib; ln -sf libcrypto.so.* libcrypto.so)
install -m 0755 ./build/ssl/libssl.so.* %{buildroot}%{openssl_prefix}/lib
(cd %{buildroot}%{openssl_prefix}/lib; ln -sf libssl.so.* libssl.so)
install -m 0644 ./include/openssl/*.h %{buildroot}%{openssl_prefix}/include/openssl

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{openssl_prefix}/lib/*

%files devel
%defattr(-,root,root,-)
%{openssl_prefix}/include/*

%changelog
* Mon Nov 22 2021 Jiahao (wangjiahao@openresty.com) 20211122
- upgrade openresty boringssl to 20211122.

* Sun Nov 14 2021 makerpm 20211114
- initial build for OpenSSL 20211114
