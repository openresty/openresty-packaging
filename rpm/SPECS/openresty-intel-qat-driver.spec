Name:               openresty-intel-qat-driver
Version:            1.7.l.4.11.0
Release:            1%{?dist}
Summary:            Intel's QAT driver for Linux

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            GPL
URL:                https://01.org/packet-processing/intel%C2%AE-quickassist-technology-drivers-and-patches
Source0:            https://01.org/sites/default/files/downloads//qat%{version}-00001.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, ccache

AutoReqProv:        no

%define qat_driver_prefix   /usr/local/openresty/intel-qat-driver
%global _default_patch_fuzz 1

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{name}-%{version}"; \
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
Intel QuickAssist Technology Driver for Linux*


%package devel

Summary:            Intel QuickAssist Technology Driver for Linux*
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
Provides C header and static library for OpenResty's OpenSSL QAT engine library.


%prep
# %setup -q -n %{name}-%{version}
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
tar xf %{_topdir}/SOURCES/qat%{version}-00001.tar.gz

# %patch0 -p1
#%patch1 -p1


%build

./configure --prefix=%{qat_driver_prefix}

make CC='ccache gcc -fdiagnostics-color=always' %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{qat_driver_prefix}/lib
mkdir -p %{buildroot}%{qat_driver_prefix}/build
mkdir -p %{buildroot}%{qat_driver_prefix}/quickassist
mkdir -p %{buildroot}%{qat_driver_prefix}/quickassist/utilities/libusdm_drv
mkdir -p %{buildroot}%{qat_driver_prefix}/quickassist/lookaside/access_layer

install build/libusdm_drv_s.so %{buildroot}%{qat_driver_prefix}/lib/
install build/libqat_s.so %{buildroot}%{qat_driver_prefix}/lib/
install build/libusdm_drv_s.so %{buildroot}%{qat_driver_prefix}/build/
install build/libqat_s.so %{buildroot}%{qat_driver_prefix}/build/

cp -r quickassist/include/ %{buildroot}%{qat_driver_prefix}/quickassist/
cp -r quickassist/lookaside/access_layer/include %{buildroot}%{qat_driver_prefix}/quickassist/lookaside/access_layer/
cp quickassist/utilities/libusdm_drv/*.h %{buildroot}%{qat_driver_prefix}/quickassist/utilities/libusdm_drv/

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{qat_driver_prefix}/lib/*.so*
%attr(0755,root,root) %{qat_driver_prefix}/build/*.so*


%files devel
%defattr(-,root,root,-)

%{qat_driver_prefix}/quickassist/include/*.h
%{qat_driver_prefix}/quickassist/include/*/*.h
%{qat_driver_prefix}/quickassist/utilities/libusdm_drv/*.h
%{qat_driver_prefix}/quickassist/lookaside/access_layer/include/*.h

%changelog
* Tue Dec 15 2020 LI Geng 1.7.l.4.11.0
- initial build for intel qat driver v1.7.l.4.11.0
