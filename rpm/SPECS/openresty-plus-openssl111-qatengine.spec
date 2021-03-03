Name:               openresty-plus-openssl111-qatengine
Version:            0.6.4
Release:            1%{?dist}
Summary:            QAT Engine for OpenResty's OpenSSL library

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://github.com/intel/QAT_Engine
Source0:            https://github.com/intel/QAT_Engine/archive/v%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make
BuildRequires:      openresty-plus-openssl111-devel >= 1.1.1i
BuildRequires:      openresty-intel-qat-driver-devel >= 1.7.l.4.11.0
Requires:           openresty-plus-openssl111 >= 1.1.1i

AutoReqProv:        no

%define openssl_prefix      /usr/local/openresty-plus/openssl111
%define qat_driver_prefix      /usr/local/openresty/intel-qat-driver
%define ext QAT_Engine
%global _default_patch_fuzz 1

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{ext}-%{version}"; \
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
This OpenSSL QAT engine library build is specifically for OpenResty uses. It may contain
custom patches from OpenResty.


%package devel

Summary:            Development files for OpenResty's OpenSSL library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
Provides C header and static library for OpenResty's OpenSSL QAT engine library.


%prep
%setup -q -n %{ext}-%{version}

# %patch0 -p1
#%patch1 -p1


%build
./autogen.sh

./configure --with-qat_dir=%{qat_driver_prefix} --with-openssl_install_dir=%{openssl_prefix} \
            --disable-qat_lenstra_protection \
            --enable-qat_small_pkt_offload \
            --enable-qat_hkdf
#            --enable-qat_contig_mem \
#            --enable-multi_thread \

# export MULTI_THREAD_MEMUTILS=1

make CC='ccache gcc -fdiagnostics-color=always' %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

chmod 0755 %{buildroot}%{openssl_prefix}/lib/engines-1.1/*.so*

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{openssl_prefix}/lib/engines-1.1/*.so*
%attr(0755,root,root) %{openssl_prefix}/lib/engines-1.1/*.la*


%files devel
%defattr(-,root,root,-)

#%{openssl_prefix}/include/*
#%{openssl_prefix}/lib/engines-1.1/*.a


%changelog
* Tue Jan 29 2021 LI Geng 0.6.4
- initial build for OpenSSL QAT engine v0.6.4
