Name:       openresty-pcre2-asan
Version:    10.42
Release:    1%{?dist}
Summary:    Perl-compatible regular expression library

Group:      System Environment/Libraries

License:    BSD
URL:        https://github.com/PCRE2Project/pcre2
Source0:    https://github.com/PCRE2Project/pcre2/releases/download/pcre2-%{version}/pcre2-%{version}.tar.gz

BuildRequires:  coreutils, gcc, make
BuildRequires:  ccache, sed

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

%define pcre2_prefix /usr/local/openresty-asan/pcre2

%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers. This package provides support for strings in 8-bit and UTF-8
encodings.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/pcre2-%{version}"; \
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
Summary:    Development files for %{name}

Requires:       %{name} = %{version}

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

%description devel
Development files (headers, libraries for dynamic linking, documentation)
for %{name}.  The header file for the POSIX-style functions is called
pcre2posix.h.

%prep
%setup -q -n pcre2-%{version}

%build
CFLAGS="-fPIC -g -O2 -fno-omit-frame-pointer" ./configure \
    --prefix=%{pcre2_prefix} \
    --libdir=%{pcre2_prefix}/lib \
    --enable-jit \
    --enable-pcre2grep-jit \
    --disable-bsr-anycrlf \
    --disable-coverage \
    --disable-ebcdic \
    --disable-fuzz-support \
    --disable-jit-sealloc \
    --disable-never-backslash-C \
    --enable-newline-is-lf \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --enable-pcre2grep-callout \
    --enable-pcre2grep-callout-fork \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
    --disable-pcre2test-libedit \
    --enable-percent-zt \
    --disable-rebuild-chartables \
    --enable-shared \
    --disable-static \
    --disable-silent-rules \
    --enable-unicode \
    --disable-valgrind
make CC='ccache gcc -fdiagnostics-color=always -fsanitize=address' -j`nproc`

%install
make install DESTDIR=%{buildroot}

# Get rid of unneeded *.la files
rm -rf $RPM_BUILD_ROOT/%{pcre2_prefix}/lib/*.la
rm -rf $RPM_BUILD_ROOT%{pcre2_prefix}/share
rm -rf $RPM_BUILD_ROOT/%{pcre2_prefix}/bin

export QA_RPATHS=$[ 0x0002 ]

%files
%dir %{pcre2_prefix}
%dir %{pcre2_prefix}/lib
%{pcre2_prefix}/lib/libpcre2-8.so.0*
%{pcre2_prefix}/lib/libpcre2-posix.so.3*
%{pcre2_prefix}/lib/libpcre2-16.so.0*
%{pcre2_prefix}/lib/libpcre2-32.so.0*

%files devel
%dir %{pcre2_prefix}/include
%{pcre2_prefix}/lib/*.so
%{pcre2_prefix}/lib/pkgconfig/*
%{pcre2_prefix}/include/*.h

%changelog
* Mon Nov 27 2023 Yichun Zhang (agentzh) 10.42-2
- update the packaging script.
* Mon Nov 27 2023 Yichun Zhang (agentzh) 10.42-1
- upgraded PCRE2 to 10.42.
* Tue Mar 29 2022 Jiahao Wang <wangjiahao@openresty.com> - 10.39-1
- upgraded pcre2 to 10.39.
