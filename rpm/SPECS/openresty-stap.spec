Name:           openresty-stap
Version:        4.2.0.7
Release:        1%{?dist}
Summary:        OpenResty's fork of SystemTap
Group:          Development/System
License:        GPLv2+
URL:            http://sourceware.org/systemtap/
Provides:       openresty-stap

Source0:        systemtap-plus-%{version}.tar.gz

AutoReqProv:    no

%define _rpmmacrodir %{_rpmconfigdir}/macros.d

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%define stap_prefix %{_usr}/local/%{name}

%define eu_prefix %{_usr}/local/openresty-elfutils

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/systemtap-plus-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}


%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ccache, gcc-c++
BuildRequires: gettext-devel
BuildRequires: m4
BuildRequires: zlib-devel
BuildRequires: xz-devel
BuildRequires: bzip2-devel
BuildRequires: openresty-elfutils-devel >= 0.176.6-3

Requires: bzip2-libs
Requires: xz-libs
Requires: zlib
Requires: make
Requires: openresty-stap-runtime = %{version}-%{release}
Requires: openresty-elfutils >= 0.176.6-3

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
AutoReqProv:    no
URL: http://sourceware.org/systemtap/


%description sdt-devel
OpenResty's fork of SystemTap sdt-devel includes the <sys/sdt.h> header file
used for static instrumentation compiled into userspace programs and libraries,
along with the optional dtrace-compatibility preprocessor to process related
.d files into tracing-macro-laden .h headers.


%prep
%setup -q -n systemtap-plus-%{version}


%build
./configure \
        --prefix=%{stap_prefix} \
        --disable-docs --disable-publican \
        --without-nss \
        --without-openssl \
        --without-avahi \
        --without-bpf \
        --without-python2-probes \
        --without-python3-probes \
        --disable-refdocs \
        CC='ccache gcc -fdiagnostics-color=always' \
        CXX='ccache g++ -fdiagnostics-color=always' \
        CFLAGS='-I%{eu_prefix}/include -g3 -O2' \
        CXXFLAGS='-I%{eu_prefix}/include -g3 -O2' \
        LDFLAGS='-L%{eu_prefix}/lib -Wl,-rpath,%{eu_prefix}/lib'

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# Because "make install" may install staprun with whatever mode, the
# post-processing programs rpmbuild runs won't be able to read it.
# So, we change permissions so that they can read it.  We'll set the
# permissions back to 04110 in the %files section below.
chmod 755 %{buildroot}%{stap_prefix}/bin/staprun

#install the useful stap-prep script
install -c -m 755 stap-prep %{buildroot}%{stap_prefix}/bin/stap-prep

#install -D -m 644 macros.systemtap %{buildroot}%{_rpmmacrodir}/macros.systemtap

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


%files runtime
%defattr(-,root,root)
%attr(4110,root,stapusr) %{stap_prefix}/bin/staprun
%{stap_prefix}/bin/stapsh
%{stap_prefix}/bin/stap-merge
%dir %{stap_prefix}/libexec/systemtap
%{stap_prefix}/libexec/systemtap/stapio


%files sdt-devel
%defattr(-,root,root)
%{stap_prefix}/bin/dtrace
%{stap_prefix}/include/sys/sdt.h
%{stap_prefix}/include/sys/sdt-config.h

# ------------------------------------------------------------------------

%changelog
* Fri Sep 13 2019 Yichun Zhang (agentzh) 4.2.0.7-1
- upgraded openresty-stap to 4.2.0.7.
* Thu Aug 1 2019 Yichun Zhang (agentzh) 4.2.0.6-1
- upgraded openresty-stap to 4.2.0.6.
* Thu Aug 1 2019 Yichun Zhang (agentzh) 4.2.0.5-1
- upgraded openresty-stap to 4.2.0.5.
* Mon Jul 29 2019 Yichun Zhang (agentzh) 4.2.0.4-1
- upgraded openresty-stap to 4.2.0.4.
* Mon Jul 29 2019 Yichun Zhang (agentzh) 4.2.0.3-1
- upgraded openresty-stap to 4.2.0.3.
* Wed Jun 19 2019 Yichun Zhang (agentzh) 4.2.0.2-1
- upgraded openresty-stap to 4.2.0.2.
* Wed Jun 19 2019 Yichun Zhang (agentzh) 4.2.0.1-1
- upgraded openresty-stap to 4.2.0.1.
* Tue Sep 18 2018 Yichun Zhang 3.3.0.3
- upgraded to 3.3.0.3.
* Mon Aug 27 2018 Ming Wen 3.3.0.2
- initial build for openresty-stap.
