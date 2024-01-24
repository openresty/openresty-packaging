Name:           openresty-elfutils
Version:        0.190.1
Release:        1%{?dist}
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
%define libdemangle_prefix %{_usr}/local/openresty-libdemangle

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ccache, gcc >= 4.1.2-33
BuildRequires: glibc >= 2.7
BuildRequires: bison >= 1.875
BuildRequires: flex >= 2.5.4a
BuildRequires: m4
BuildRequires: gettext
BuildRequires: zlib-devel

%if 0%{?suse_version}
BuildRequires: libbz2-devel
%else
BuildRequires: bzip2-devel
%endif

BuildRequires: xz-devel
BuildRequires: gcc-c++
BuildRequires: autoconf
BuildRequires: openresty-yajl-devel >= 2.1.0.3-2
BuildRequires: openresty-libdemangle-devel
BuildRequires: gawk
BuildRequires: sed

Requires: glibc >= 2.7

%if 0%{?suse_version}
Requires: libstdc++6
%else
Requires: libstdc++
%endif

Requires: openresty-yajl >= 2.1.0.3-2
Requires: openresty-libdemangle

%if 0%{?suse_version}
Requires: libbz2-1
%else
Requires: bzip2-libs
%endif

%if 0%{?suse_version}
Requires: liblzma5
%else
Requires: xz-libs
%endif

%description
OpenResty's fork of SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system. The base systemtap package contains/requires
the components needed to locally develop and execute systemtap scripts.

# ------------------------------------------------------------------------


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/elfutils-plus-%{version}"; \
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

%if 0%{?fedora} >= 34
%define EXTRA_CFLAGS "-Wno-array-parameter"
%define yflags YFLAGS="-Wno-yacc"
%else
%define EXTRA_CFLAGS ""
%define yflags ""
%endif


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
./configure \
    --prefix="%{eu_prefix}" \
    --libdir="%{eu_prefix}/lib" \
    LIBS='-Wl,-rpath,%{eu_prefix}/lib:%{yajl_prefix}/lib:%{libdemangle_prefix}/lib -L%{yajl_prefix}/lib -lyajl -L%{libdemangle_prefix}/lib -ldemangle -lrt' \
    CC='ccache gcc -fdiagnostics-color=always' \
    CFLAGS="%{EXTRA_CFLAGS} -fPIC -I%{yajl_prefix}/include -I%{libdemangle_prefix}/include -g3 -O2" \
    %{yflags} \
    --enable-maintainer-mode \
    --disable-debuginfod \
    --enable-libdebuginfod=dummy

sed -i 's#^dso_LDFLAGS = #dso_LDFLAGS = -Wl,-rpath,%{eu_prefix}/lib:%{yajl_prefix}/lib:%{libdemangle_prefix}/lib  #' \
    `find . -name Makefile`

make -j`nproc`


%install

export QA_RPATHS=$(( 0x0001|0x0010|0x0002 ))

make install DESTDIR=%{buildroot}
ln -sf %{eu_prefix}/bin/eu-readelf %{buildroot}/%{eu_prefix}/bin/eu-readelf2

# remove useless files
rm -rf %{buildroot}%{eu_prefix}/share/man
rm -f %{buildroot}%{eu_prefix}/etc/profile.d/debuginfod.csh
rm -f %{buildroot}%{eu_prefix}/etc/profile.d/debuginfod.sh

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%defattr(-,root,root)
%dir %{eu_prefix}
%dir %{eu_prefix}/bin
%dir %{eu_prefix}/lib
%dir %{eu_prefix}/share
%{eu_prefix}/bin/*
%{eu_prefix}/share/*
%{eu_prefix}/lib/*.so.*
%{eu_prefix}/lib/*.so


%files devel
%defattr(-,root,root)
%dir %{eu_prefix}/include
%dir %{eu_prefix}/lib/pkgconfig
%{eu_prefix}/include/*
%{eu_prefix}/lib/pkgconfig/*
%{eu_prefix}/lib/*.a


# ------------------------------------------------------------------------

%changelog
* Tue Jan 23 2024 Yichun Zhang (agentzh) 0.190.1-1
- upgraded elfutils-plus to 0.190.1.
* Mon Jan 15 2024 Yichun Zhang (agentzh) 0.188.15-1
- upgraded elfutils-plus to 0.188.15.
* Wed Nov 29 2023 Yichun Zhang (agentzh) 0.188.14-1
- upgraded elfutils-plus to 0.188.14.
* Wed Oct 11 2023 Yichun Zhang (agentzh) 0.188.13-1
- upgraded elfutils-plus to 0.188.13.
* Mon Sep 18 2023 Yichun Zhang (agentzh) 0.188.11-1
- upgraded elfutils-plus to 0.188.11.
* Wed Sep 13 2023 Yichun Zhang (agentzh) 0.188.10-1
- upgraded elfutils-plus to 0.188.10.
* Mon Sep 4 2023 Yichun Zhang (agentzh) 0.188.9-1
- upgraded elfutils-plus to 0.188.9.
* Wed Jul 26 2023 Yichun Zhang (agentzh) 0.188.8-1
- upgraded elfutils-plus to 0.188.8.
* Wed Jul 26 2023 Yichun Zhang (agentzh) 0.188.7-1
- upgraded elfutils-plus to 0.188.7.
* Thu Jun 29 2023 Yichun Zhang (agentzh) 0.188.6-1
- upgraded elfutils-plus to 0.188.6.
* Wed Jun 14 2023 Yichun Zhang (agentzh) 0.188.5-1
- upgraded elfutils-plus to 0.188.5.
* Thu Jun 8 2023 Yichun Zhang (agentzh) 0.188.4-1
- upgraded elfutils-plus to 0.188.4.
* Tue May 23 2023 Yichun Zhang (agentzh) 0.188.3-1
- upgraded elfutils-plus to 0.188.3.
* Fri Feb 17 2023 Yichun Zhang (agentzh) 0.188.2-1
- upgraded elfutils-plus to 0.188.2.
* Thu Feb 9 2023 Yichun Zhang (agentzh) 0.188.1-1
- upgraded elfutils-plus to 0.188.1.
* Wed Aug 24 2022 Yichun Zhang (agentzh) 0.187.2-1
- upgraded elfutils-plus to 0.187.2.
* Tue Jun 21 2022 Yichun Zhang (agentzh) 0.187.1-1
- upgraded elfutils-plus to 0.187.1.
* Fri Apr 29 2022 Yichun Zhang (agentzh) 0.185.4-1
- upgraded elfutils-plus to 0.185.4.
* Wed Apr 27 2022 Yichun Zhang (agentzh) 0.185.3-1
- upgraded elfutils-plus to 0.185.3.
* Tue Apr 19 2022 Yichun Zhang (agentzh) 0.185.2-1
- upgraded elfutils-plus to 0.185.2.
* Mon Jul 05 2021 Yichun Zhang (agentzh) 0.185.1-1
- upgraded elfutils-plus to 0.185.1.
* Tue May 18 2021 Yichun Zhang (agentzh) 0.177.13-1
- upgraded elfutils-plus to 0.177.13.
* Tue Nov 3 2020 Yichun Zhang (agentzh) 0.177.12-1
- upgraded elfutils-plus to 0.177.12.
* Sat Jul 11 2020 Yichun Zhang (agentzh) 0.177.11-1
- upgraded elfutils-plus to 0.177.11.
* Mon Jun 29 2020 Yichun Zhang (agentzh) 0.177.10-1
- upgraded elfutils-plus to 0.177.10.
* Fri Jun 12 2020 Yichun Zhang (agentzh) 0.177.9-1
- upgraded elfutils-plus to 0.177.9.
* Mon May 25 2020 Yichun Zhang (agentzh) 0.177.8-1
- upgraded elfutils-plus to 0.177.8.
* Fri May 22 2020 Yichun Zhang (agentzh) 0.177.7-1
- upgraded elfutils-plus to 0.177.7.
* Mon Mar 16 2020 Yichun Zhang (agentzh) 0.177.5-1
- upgraded elfutils-plus to 0.177.5.
* Thu Oct 31 2019 Yichun Zhang (agentzh) 0.177.4-1
- upgraded elfutils-plus to 0.177.4.
* Sun Oct 27 2019 Yichun Zhang (agentzh) 0.177.3-1
- upgraded elfutils-plus to 0.177.3.
* Mon Oct 21 2019 Yichun Zhang (agentzh) 0.177.2-1
- upgraded elfutils-plus to 0.177.2.
* Sat Jul 6 2019 Yichun Zhang (agentzh) 0.176.6-1
- upgraded elfutils-plus to 0.176.6.
* Tue Mar 20 2018 Yichun Zhang 0.176.1
- upgraded to 0.176.1
