Name:           openresty-maxminddb-asan
Version:        1.4.2.4
Release:        4%{?dist}
Summary:        gcc AddressSanitizer version for OpenResty's fork of libmaxminddb
Group:          Development/System
License:        Apache License, Version 2.
URL:            https://github.com/maxmind/libmaxminddb

Source0:        libmaxminddb-plus-%{version}.tar.gz

AutoReqProv: no

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ccache, make, gcc

%define _rpmmacrodir %{_rpmconfigdir}/macros.d

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%define _prefix %{_usr}/local/openresty-plus-asan

%if 0%{?suse_version}

%debug_package

%else
# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/libmaxminddb-plus-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%endif

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif



%description
OpenResty's fork of libmaxminddb that is to work with lua-resty-maxminddb. This is the gcc AddressSanitizer build.

# ------------------------------------------------------------------------
%prep
%setup -q -n libmaxminddb-plus-%{version}


%build
export ASAN_OPTIONS=detect_leaks=0
./configure \
    --prefix=%{_prefix} \
    CC="gcc -fsanitize=address"  \
    CFLAGS="-O1 -fno-omit-frame-pointer -g3" \
    --disable-tests

make CC="gcc -fsanitize=address" \
        CFLAGS='-O1 -fno-omit-frame-pointer -g3' \
        -j`nproc` > /dev/null


%install
install -d %{buildroot}/%{_prefix}/lualib
install ./src/.libs/libmaxminddb.so %{buildroot}/%{_prefix}/lualib/libmaxminddb.so


%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%defattr(-,root,root)
%{_prefix}/lualib/*.so

# ------------------------------------------------------------------------

%changelog
* Tue Nov 17 2020 Yichun Zhang (agentzh) 1.4.2.4-1
- upgraded libmaxminddb-plus to 1.4.2.4.
* Sat Nov 14 2020 lijunlong v1.4.2.3
- upgraded libmaxminddb-plus to v1.4.2.3.
