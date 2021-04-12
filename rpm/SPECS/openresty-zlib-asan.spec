Name:               openresty-zlib-asan
Version:            1.2.11
Release:            16%{?dist}
Summary:            Gcc AddressSanitizer version for the zlib compression library for OpenResty

Group:              System Environment/Libraries

# /contrib/dotzlib/ have Boost license
License:            zlib and Boost
URL:                http://www.zlib.net/
Source0:            http://www.zlib.net/zlib-%{version}.tar.xz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      libtool, gcc
%if 0%{?suse_version}
BuildRequires:      libasan4
%else
BuildRequires:      libasan
%endif

%if 0%{?suse_version}
Requires:           libasan4
%else
Requires:           libasan
%endif

AutoReqProv:        no

%define zlib_prefix     /usr/local/openresty-asan/zlib

%if 0%{?el6}
%undefine _missing_build_ids_terminate_build
%endif


%description
The zlib compression library for use by Openresty ONLY. This is the gcc AddressSanitizer build.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/zlib-%{version}"; \
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
Provides C header and static library for OpenResty's gcc AddressSanitizer version of zlib library.


%prep
%setup -q -n zlib-%{version}


%build
export ASAN_OPTIONS=detect_leaks=0

CC="gcc -fsanitize=address" ./configure --prefix=%{zlib_prefix}

make -j`nproc` CC="gcc -fsanitize=address" \
    CFLAGS='-O1 -fno-omit-frame-pointer -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    SFLAGS='-O1 -fno-omit-frame-pointer -fPIC -D_LARGEFILE64_SOURCE=1 -DHAVE_HIDDEN -g3' \
    LDSHARED='gcc -fsanitize=address -shared -Wl,-soname,libz.so.1,--version-script,zlib.map' \
    > /dev/stderr


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{zlib_prefix}/share
rm -f  %{buildroot}/%{zlib_prefix}/lib/*.la
rm -rf %{buildroot}/%{zlib_prefix}/lib/pkgconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{zlib_prefix}/lib/libz.so*


%files devel
%defattr(-,root,root,-)

%{zlib_prefix}/lib/*.a
%{zlib_prefix}/include/zlib.h
%{zlib_prefix}/include/zconf.h


%changelog
* Sat Jul 15 2017 Yichun Zhang (agentzh) 1.2.11-6
- specify the correct CC environment before running ./configure too.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 1.2.11-5
- restored --version-script.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 1.2.11-4
- removed linker option --version-script.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 1.2.11-3
- fixed spec for CentOS 6 regarding missing build id issues.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 1.2.11-2
- forgot to use clang -fsanitize=address to link shared libraries.
* Fri Jul 14 2017 Yichun Zhang (agentzh) 1.2.11-1
- initial build for zlib 1.2.11.
