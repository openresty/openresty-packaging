Name:           openresty-elfutils
Version:        0.176.6
Release:        3%{?dist}
Summary:        OpenResty's fork of SystemTap
Group:          Development/System
License:        LGPLv2+
URL:            http://sourceware.org/systemtap/

Source0:        elfutils-plus-%{version}.tar.gz

AutoReqProv: no

%define _rpmmacrodir %{_rpmconfigdir}/macros.d

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%define eu_prefix %{_usr}/local/%{name}

%define yajl_prefix      %{_usr}/local/openresty-yajl

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/elfutils-plus-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gcc >= 4.1.2-33
BuildRequires: glibc >= 2.7
BuildRequires: bison >= 1.875
BuildRequires: flex >= 2.5.4a
BuildRequires: m4
BuildRequires: gettext
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel
BuildRequires: gcc-c++
BuildRequires: autoconf
BuildRequires: openresty-yajl-devel
BuildRequires: gawk
BuildRequires: sed

Requires: glibc >= 2.7
Requires: libstdc++
Requires: openresty-yajl
Requires: bzip2-libs
Requires: xz-libs

%description
OpenResty's fork of SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system. The base systemtap package contains/requires
the components needed to locally develop and execute systemtap scripts.

# ------------------------------------------------------------------------

%package devel
Summary: devel files for OpenResty's fork of elfutils
Group: Development/System
License: LGPLv2+ and Public Domain
URL: http://sourceware.org/systemtap/

Requires: %{name} = %{version}


%description devel
OpenResty's fork of elfutils.


%prep
%setup -q -n elfutils-plus-%{version}


%build
autoreconf -vif

./configure \
    --prefix=%{eu_prefix} \
    LIBS='-Wl,-rpath,%{eu_prefix}/lib:%{yajl_prefix}/%{_lib} -L%{yajl_prefix}/%{_lib} -lyajl' \
    CFLAGS="-Wa,-mrelax-relocations=no -Wa,--nocompress-debug-sections -I%{yajl_prefix}/include -g3 -O2" \
    --enable-maintainer-mode

sed -i 's#^dso_LDFLAGS = #dso_LDFLAGS = -Wl,-rpath,%{eu_prefix}/lib:%{yajl_prefix}/%{_lib} #' \
    `find . -name Makefile`

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# remove useless files
rm -rf %{buildroot}%{eu_prefix}/share/man

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%defattr(-,root,root)
%{eu_prefix}/bin/*
%{eu_prefix}/share/*
%{eu_prefix}/lib/*.so.*
%{eu_prefix}/lib/*.so
%{eu_prefix}/lib/elfutils/*


%files devel
%defattr(-,root,root)
%{eu_prefix}/include/*
%{eu_prefix}/lib/pkgconfig/*
%{eu_prefix}/lib/pkgconfig
%{eu_prefix}/lib/*.a


# ------------------------------------------------------------------------

%changelog
* Sat Jul 6 2019 Yichun Zhang (agentzh) 0.176.6-1
- upgraded elfutils-plus to 0.176.6.
* Wed Mar 20 2018 Yichun Zhang 0.176.1
- upgraded to 0.176.1
