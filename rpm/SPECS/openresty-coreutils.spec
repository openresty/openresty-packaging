%define         _name   coreutils
%define         _prefix /usr/local/openresty-coreutils

Summary:        Basic system utilities
Name:           openresty-coreutils
Version:        8.32
Release:        4%{?dist}
License:        GPLv3
URL:            http://www.gnu.org/software/coreutils
Group:          System Environment/Base
Source0:        http://ftp.gnu.org/gnu/coreutils/%{_name}-%{version}.tar.xz

AutoReqProv:    no
BuildRequires:  ccache, gcc, make

%description
The Coreutils package contains utilities for showing and setting
the basic system

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{_name}-%{version}"; \
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
%setup -q -n %{_name}-%{version}

%build
CC='ccache gcc -fdiagnostics-color=always' \
    ./configure \
    --libexecdir="%{_prefix}/libexec" \
    --libdir="%{_prefix}/lib" \
    --prefix=%{_prefix} --disable-silent-rules

make -j`nproc`

%install
rm -rf %{buildroot}
make install-binPROGRAMS DESTDIR=${RPM_BUILD_ROOT}
make install-pkglibexecPROGRAMS DESTDIR=${RPM_BUILD_ROOT}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_prefix}/bin
%attr(0755,root,root) %{_prefix}/bin/*
%attr(0755,root,root) %{_prefix}/libexec/coreutils/*

%changelog
* Wed Dec 30 2020 Jiahao Wang (johnny) 8.32-2
- bugfix: added missing libstdbuf.so.

* Sat Dec 26 2020 Jiahao Wang (johnny) 8.32-1
- initial packaging.
