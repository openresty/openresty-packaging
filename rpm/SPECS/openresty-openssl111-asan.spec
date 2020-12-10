Name:               openresty-openssl111-asan
Version:            1.1.1i
Release:            1%{?dist}
Summary:            Clang AddressSanitizer Debug version of the OpenSSL library for OpenResty

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://www.openssl.org/source/openssl-%{version}.tar.gz

#Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.1e-sess_set_get_cb_yield.patch
Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.1f-sess_set_get_cb_yield.patch
#Patch1:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.0j-parallel_build_fix.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      ccache, gcc, make, perl, clang

BuildRequires:      openresty-zlib-asan-devel >= 1.2.11-6
Requires:           openresty-zlib-asan >= 1.2.11-6

AutoReqProv:        no

%define openssl_prefix      %{_usr}/local/openresty-asan/openssl111
%define zlib_prefix         /usr/local/openresty-asan/zlib
%global _default_patch_fuzz 1

%if 0%{?el6}
%undefine _missing_build_ids_terminate_build
%endif

%if 0%{?fedora} >= 28
#BuildRequires:      compiler-rt
%endif

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openssl-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%if 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%description
This is the clang AddressSanitizer version of the OpenSSL library build for OpenResty uses.


%package devel

Summary:            Clang AddressSanitizer version of development files for OpenResty's OpenSSL library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
Provides C header and static library for the clang AddressSanitizer version of OpenResty's OpenSSL library. This is the clang AddressSanitizer version.

%prep
%setup -q -n openssl-%{version}

%patch0 -p1
#%patch1 -p1


%build
export ASAN_OPTIONS=detect_leaks=0

./config \
    no-asm \
    enable-camellia enable-seed enable-rfc3779 \
    enable-cms enable-md2 enable-rc5 \
    enable-weak-ssl-ciphers \
    enable-ssl3 enable-ssl3-method \
    shared zlib -g3 -O1 -DPURIFY \
    --prefix=%{openssl_prefix} \
    --libdir=lib \
    -I%{zlib_prefix}/include \
    -L%{zlib_prefix}/lib \
    -Wl,-rpath,%{zlib_prefix}/lib:%{openssl_prefix}/lib

#sed -i 's/ -O3 / -O1 -fno-omit-frame-pointer /g' Makefile
#sed -r -i 's/^([ \t]*)LD_LIBRARY_PATH=[^\\ \t]*/\1LD_LIBRARY_PATH=/g' Makefile.shared

make %{?_smp_mflags} \
    LD_LIBRARY_PATH= \
    CC="ccache clang -fsanitize=address -fcolor-diagnostics -Qunused-arguments" \
    > /dev/stderr


%install
make install_sw DESTDIR=%{buildroot}

chmod +w %{buildroot}%{openssl_prefix}/lib/*.so
chmod +w %{buildroot}%{openssl_prefix}/lib/*/*.so

rm -rf %{buildroot}%{openssl_prefix}/bin/c_rehash
rm -rf %{buildroot}%{openssl_prefix}/lib/pkgconfig
rm -rf %{buildroot}%{openssl_prefix}/misc

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{openssl_prefix}/bin/openssl
%attr(0755,root,root) %{openssl_prefix}/lib/*.so*
%attr(0755,root,root) %{openssl_prefix}/lib/*/*.so*


%files devel
%defattr(-,root,root,-)

%{openssl_prefix}/include/*
%attr(0755,root,root) %{openssl_prefix}/lib/*.a


%changelog
* Thu Dec 10 2020 Yichun Zhang (agentzh) 1.1.1i-1
- upgraded OpenSSL to 1.1.1i.
* Mon May 14 2018 Yichun Zhang (agentzh) 1.1.0h-1
- upgraded openresty-openssl to 1.1.0h.
* Thu Apr 19 2018  Yichun Zhang (agentzh) 1.0.2n-1
- upgraded openssl to 1.0.2n.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 1.0.2k-2
- bugfix: forgot to add clang to the build dep list.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 1.0.2k-1
- initial build for OpenSSL 1.0.2k.
