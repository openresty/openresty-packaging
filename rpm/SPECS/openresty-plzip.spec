Name:           openresty-plzip
Version:        1.8
Release:        3%{?dist}
Summary:        OpenResty's fork of plzip.

Group:          Development/System
License:        GPLv3+
URL:            http://www.nongnu.org/lzip/lzip.html

%define prefix  %{_usr}/local/openresty-plzip
%define lzlib_version 1.11
%define lzlib_prefix %{prefix}

Source0:        http://download.savannah.gnu.org/releases/lzip/plzip/plzip-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/lzlib/lzlib-%{lzlib_version}.tar.gz

BuildRequires:  ccache, gcc, make, gcc-c++

%description
Lzip compresses data using LZMA (Lempel-Ziv-Markov chain-Algorithm). It
supports integrity checking using CRC (Cyclic Redundancy Check). To archive
multiple files, tar can be used with lzip. Please note, that the lzip file
format (.lz) is not compatible with the lzma file format (.lzma).


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/plzip-%{version}"; \
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
%setup -q -b 1 -n plzip-%{version}

%build
mv ${PWD}/../lzlib-%{lzlib_version} lzlib

# build lzlib first
cd lzlib \
    && ./configure --prefix=/lzlib \
    CC='ccache gcc -fdiagnostics-color=always' \
    CXXFLAGS='-Wall -W -O2 -g3' \
    && make %{?_smp_mflags} \
    && make install DESTDIR='%{_builddir}/%{?buildsubdir}' \
    && cd -

./configure --prefix=%{prefix} \
    CC='ccache gcc -fdiagnostics-color=always' \
    CXXFLAGS="-Wall -W -O2 -g3 -I%{_builddir}/%{?buildsubdir}/lzlib/include" \
    LDFLAGS="-L%{_builddir}/%{?buildsubdir}/lzlib/lib" \
    && make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install-bin DESTDIR=%{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{prefix}/bin/plzip


%changelog
* Tue Nov 05 2019 Johnny Wang <wangjiahao@openresty.com>
- initial packaging
