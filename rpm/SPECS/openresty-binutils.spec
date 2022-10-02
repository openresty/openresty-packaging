%define binutils_name binutils-gdb-plus
%define binutils_prefix %{_usr}/local/openresty-binutils

Name:           openresty-binutils
Version:        2.39.0.1
Release:        4%{?dist}
Summary:        OpenResty's fork of binutils.
Group:          Development/System
License:        GPLv3+
URL:            https://sourceware.org/binutils

Source0:        %{binutils_name}-%{version}.tar.gz

AutoReqProv: no

%define _rpmmacrodir %{_rpmconfigdir}/macros.d

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ccache, gcc >= 4.1.2-33
BuildRequires: texinfo >= 4.0, gettext, flex, bison, zlib-devel

%description
OpenResty's fork of Binutils.

Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).

# ------------------------------------------------------------------------


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{binutils_name}-%{version}"; \
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
%setup -q -n %{binutils_name}-%{version}


%build

./configure \
    --prefix=%{binutils_prefix} --disable-gas --disable-gold \
    --disable-ar --disable-gprof --disable-gprofng --disable-dlltool --disable-ranlib --disable-windmc \
    --disable-windres --disable-nlmconv --with-system-zlib --disable-gdb \
    --disable-bdf --disable-etc --disable-gnulib --disable-intl \
    --disable-libdecnumber --disable-sim --disable-readline \
    --enable-targets=all \
    --disable-libquadmath \
    CFLAGS='-Wno-error -g -O2 -fPIC' \
    CC='ccache gcc -fdiagnostics-color=always'

make -j`nproc` all-binutils

%install
make install-binutils DESTDIR=%{buildroot}

# remove useless files
rm -rf %{buildroot}%{binutils_prefix}/share/man
rm -rf %{buildroot}%{binutils_prefix}/share/info
rm -rf %{buildroot}%{binutils_prefix}/share/locale
rm -rf %{buildroot}%{binutils_prefix}/lib
rm -rf %{buildroot}%{binutils_prefix}/include
rm -rf %{buildroot}%{binutils_prefix}/x86_64-pc-linux-gnu
rm -f %{buildroot}%{binutils_prefix}/bin/elfedit

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%defattr(-,root,root)
%{binutils_prefix}/bin/*


# ------------------------------------------------------------------------

%changelog
* Mon Aug 22 2022 Yichun Zhang (agentzh) 2.39.0.1-2
- upgraded binutils-gdb-plus to 2.39.0.1.
* Tue Aug 16 2022 Yichun Zhang (agentzh) 2.39.0.1-1
- upgraded binutils-gdb-plus to 2.39.0.1.
* Thu Dec 9 2021 Yichun Zhang (agentzh) 2.37.0.1-1
- upgraded binutils-gdb-plus to 2.37.0.1.
* Wed Jul 07 2021 lijunlong (lijunlong@openresty.com)
- update to version 2.36.1
* Sat Nov 02 2019 Jiahao Wang (johnny)
- initial packaging
