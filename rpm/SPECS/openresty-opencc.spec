Name:               openresty-opencc
Version:            1.1.6
Release:            1%{?dist}
Summary:            Open Chinese Convert is an opensource project for conversions between Traditional Chinese, Simplified Chinese and Japanese Kanji (Shinjitai). 

Group:              Development/Tools

# /contrib/dotzlib/ have Boost license
License:            Apache-2.0 license
URL:                https://opencc.byvoid.com/
Source0:            https://github.com/BYVoid/OpenCC/archive/refs/tags/ver.1.1.6.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext
BuildRequires:  cmake
BuildRequires:  python3

AutoReqProv:    no

%define opencc_prefix     /usr/local/openresty-opencc


%description
Open Chinese Convert is an opensource project for conversions between Traditional Chinese, Simplified Chinese and Japanese Kanji (Shinjitai). 

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/OpenCC-ver.%{version}"; \
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

Summary:            Development files for OpenResty's zlib library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty's zlib library.


%prep
%setup -q -n OpenCC-ver.%{version}


%build
mkdir build
CXXFLAGS="-O3 -g" LDFLAGS="-Wl,-rpath,%{opencc_prefix}/lib" cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr/local/openresty-opencc -DENABLE_GETTEXT:BOOL=ON -DCMAKE_BUILD_TYPE=Release

make -j`nproc` PREFIX=%{opencc_prefix}


%install
make install DESTDIR=%{buildroot} PREFIX=%{opencc_prefix}
rm -f  %{buildroot}/%{opencc_prefix}/lib/*.la
rm -rf %{buildroot}/%{opencc_prefix}/lib/pkgconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%dir %{opencc_prefix}
%dir %{opencc_prefix}/lib
%dir %{opencc_prefix}/bin
%dir %{opencc_prefix}/share/opencc

%attr(0755,root,root) %{opencc_prefix}/lib/libopencc.so*
%attr(0755,root,root) %{opencc_prefix}/bin/opencc
%attr(0755,root,root) %{opencc_prefix}/bin/opencc_dict
%attr(0755,root,root) %{opencc_prefix}/bin/opencc_phrase_extract
%attr(0644,root,root) %{opencc_prefix}/share/opencc/*


%files devel
%defattr(-,root,root,-)

%dir %{opencc_prefix}/include
%{opencc_prefix}/include/opencc/*.hpp
%{opencc_prefix}/include/opencc/*.h


%changelog
* Sun Apr 23 2023 Yichun Zhang (agentzh) 1.1.6-1
- upgraded openresty-opencc to 1.1.6-1
