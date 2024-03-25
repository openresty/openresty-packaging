Name:           openresty-zstd
Version:        1.5.5
Release:        2%{?dist}
Summary:        OpenResty's fork of zstd.

Group:          Development/System
License:        Proprietary
URL:            https://facebook.github.io/zstd/

%define prefix  %{_usr}/local/openresty-zstd

Source0:        https://github.com/facebook/zstd/archive/refs/tags/v%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  ccache, gcc, make

%description
Zstandard, or zstd as short version, is a fast lossless compression algorithm, targeting real-time compression scenarios at zlib-level and better compression ratios.
It's backed by a very fast entropy stage, provided by Huff0 and FSE library.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/zstd-%{version}"; \
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
%setup -q -n zstd-%{version}

%build

HAVE_ZLIB=0 HAVE_LZMA=0 LDLIBS=-lrt make -j`nproc`


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=%{buildroot}%{prefix}

rm -rf %{buildroot}%{prefix}/share
rm -rf %{buildroot}%{prefix}/include
rm -rf %{buildroot}%{prefix}/lib/*.a
rm -rf %{buildroot}%{prefix}/lib/pkgconfig

%clean
rm -rf $RPM_BUILD_ROOT


%files
%dir %{prefix}
%dir %{prefix}/bin
%dir %{prefix}/lib
%defattr(-,root,root,-)
%{prefix}/bin/zstd
%{prefix}/bin/unzstd
%{prefix}/bin/zstdcat
%{prefix}/bin/zstdgrep
%{prefix}/bin/zstdless
%{prefix}/bin/zstdmt
%{prefix}/lib/libzstd.so
%{prefix}/lib/libzstd.so.*


%changelog
* Thu Mar 14 2024 Hui Wanghui <wanghui@openresty.com>
- initial packaging
