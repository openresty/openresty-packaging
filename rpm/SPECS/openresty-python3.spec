Name:           openresty-python3
Version:        3.7.3
Release:        4%{?dist}
Summary:        python3 for OpenResty

Group:          Development/Languages
License:        PSFL
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz

AutoReqProv:    no


%define _prefix /usr/local/openresty-python3

%global __os_install_post     %{nil}


# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/Python-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires: glibc-devel
BuildRequires: ccache, gcc
BuildRequires: openssl-devel
BuildRequires: make

Requires: openssl


%description
This is OpenResty's python3 package


%package devel
Summary: Libraries and header files needed for Python development
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.


%prep
%setup -q -n Python-%{version}


%build

export PYTHONPATH=

./configure --prefix=%{_prefix} --enable-shared --enable-ipv6 \
    --without-ensurepip \
    CC='ccache gcc -g3 -fdiagnostics-color=always' \
    LDFLAGS="-L. -L%{_prefix}/lib -Wl,-rpath,%{_prefix}/lib" \
    CFLAGS="-g3"

make %{?_smp_mflags} > /dev/null


%install
make \
    DESTDIR=%{buildroot} \
    INSTALL="install -p" \
    install > /dev/null

find %{buildroot} -type f -print0 | xargs -0 chmod u+w

rm -rf %{buildroot}%{_prefix}/share
( find %{buildroot}%{_prefix}/lib -type d -name 'test' -exec rm -rf "{}" \; || exit 0 )
( find %{buildroot}%{_prefix}/lib -type d -name 'tests' -exec rm -rf "{}" \; || exit 0 )
( find %{buildroot}%{_prefix}/lib -type d -name 'unittest' -exec rm -rf "{}" \; || exit 0 )
#( find %{buildroot}%{_prefix}/lib -type d -name '__pycache__' -exec rm -r "{}" \; || exit 0 )


%files
%defattr(-, root, root)
%{_prefix}/bin/*
%{_prefix}/lib/*.so
%{_prefix}/lib/*.so.*
%{_prefix}/lib/python*/*


%files devel
%defattr(-, root, root)
%{_prefix}/include/*
%{_prefix}/lib/pkgconfig/*


%clean
rm -rf %{buildroot}


%changelog
