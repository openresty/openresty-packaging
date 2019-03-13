Name:           openresty-stap
Version:        4.0.0.4
Release:        1%{?dist}
Summary:        OpenResty's fork of SystemTap
Group:          Development/System
License:        GPLv2+
URL:            http://sourceware.org/systemtap/
Provides:       openresty-stap

Source0: systemtap-plus-%{version}.tar.gz

AutoReqProv: no

%define _rpmmacrodir %{_rpmconfigdir}/macros.d

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%define stap_prefix %{_usr}/local/%{name}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%define elfutils_version 0.173
Source1: https://sourceware.org/elfutils/ftp/%{elfutils_version}/elfutils-%{elfutils_version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc-c++
BuildRequires: gettext-devel
BuildRequires: nss-devel avahi-devel
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(avahi-client)
BuildRequires: m4
BuildRequires: zlib-devel
BuildRequires: xz-devel
BuildRequires: python-setuptools
BuildRequires: avahi-devel

Requires: xz-libs
Requires: kernel-devel-uname-r
Requires: gcc make
Requires: openresty-stap-runtime = %{version}-%{release}
Requires: avahi-libs

%description
OpenResty's fork of SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system. The base systemtap package contains/requires
the components needed to locally develop and execute systemtap scripts.

# ------------------------------------------------------------------------

%package runtime
Summary: Programmable system-wide instrumentation system - runtime (OpenResty's fork of SystemTap)
Group: Development/System
License: GPLv2+
URL: http://sourceware.org/systemtap/
Requires(pre): shadow-utils

%description runtime
OpenResty's fork of SystemTap runtime contains the components needed to execute
a systemtap script that was already compiled into a module
using a local or remote systemtap-devel installation.


%package sdt-devel
Summary: Static probe support tools (OpenResty's fork of SystemTap)
Group: Development/System
License: GPLv2+ and Public Domain
URL: http://sourceware.org/systemtap/


%description sdt-devel
OpenResty's fork of SystemTap sdt-devel includes the <sys/sdt.h> header file
used for static instrumentation compiled into userspace programs and libraries,
along with the optional dtrace-compatibility preprocessor to process related
.d files into tracing-macro-laden .h headers.


%prep
%setup -D -q -n elfutils-%{elfutils_version} -b 1
%setup -q -n systemtap-plus-%{version}


%build
./configure --with-elfutils=../elfutils-%{elfutils_version} \
        --prefix=%{stap_prefix} \
        --disable-docs --disable-publican \
        --without-python2-probes \
        --without-python3-probes \
        --disable-refdocs

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Because "make install" may install staprun with whatever mode, the
# post-processing programs rpmbuild runs won't be able to read it.
# So, we change permissions so that they can read it.  We'll set the
# permissions back to 04110 in the %files section below.
chmod 755 %{buildroot}%{stap_prefix}/bin/staprun

#install the useful stap-prep script
install -c -m 755 stap-prep %{buildroot}%{stap_prefix}/bin/stap-prep

install -D -m 644 macros.systemtap %{buildroot}%{_rpmmacrodir}/macros.systemtap

# remove useless files
rm -rf %{buildroot}%{stap_prefix}/share/man
rm -rf %{buildroot}%{stap_prefix}/share/systemtap/examples
rm -rf %{buildroot}%{stap_prefix}/share/locale
rm -rf %{buildroot}%{stap_prefix}/lib64/python2.7
rm -f %{buildroot}%{stap_prefix}/bin/stap-server
rm -f %{buildroot}%{stap_prefix}/bin/stapbpf
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-env
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-gen-cert
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-serverd
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-sign-module
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-start-server
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-stop-server
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/python/stap-resolve-module-function.py*

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%{stap_prefix}/bin/stap
%{stap_prefix}/bin/stap-prep
%{stap_prefix}/bin/stap-report
%dir %{stap_prefix}/share/systemtap
%{stap_prefix}/share/systemtap/runtime
%{stap_prefix}/share/systemtap/tapset
%dir %{stap_prefix}/lib/systemtap
%{stap_prefix}/lib/systemtap/lib*.so*


%files runtime
%defattr(-,root,root)
%attr(4110,root,stapusr) %{stap_prefix}/bin/staprun
%{stap_prefix}/bin/stapsh
%{stap_prefix}/bin/stap-merge
%{stap_prefix}/bin/stap-report
%dir %{stap_prefix}/libexec/systemtap
%{stap_prefix}/libexec/systemtap/stapio
%{stap_prefix}/libexec/systemtap/stap-authorize-cert


%files sdt-devel
%defattr(-,root,root)
%{stap_prefix}/bin/dtrace
%{stap_prefix}/include/sys/sdt.h
%{stap_prefix}/include/sys/sdt-config.h
%{_rpmmacrodir}/macros.systemtap

# ------------------------------------------------------------------------

%changelog
* Tue Sep 18 2018 Yichun Zhang 3.3.0.3
- upgraded to 3.3.0.3.
* Mon Aug 27 2018 Ming Wen 3.3.0.2
- initial build for openresty-stap.
