Name:           openresty-python3
Version:        3.7.14
Release:        3%{?dist}
Summary:        python3 for OpenResty

Group:          Development/Languages
License:        PSFL
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz

AutoReqProv:    no


%define _prefix     /usr/local/openresty-python3
%define ssl_prefix  /usr/local/openresty-plus/openssl111

%global __os_install_post     %{nil}


BuildRequires: glibc-devel
BuildRequires: ccache, gcc
BuildRequires: openresty-plus-openssl111-devel >= 1.1.1h-1
BuildRequires: make

%if "%{?_vendor}" == "mariner"
BuildRequires: uuid-devel
%else
BuildRequires: libuuid-devel
%endif

Requires: openresty-plus-openssl111 >= 1.1.1i-1
Requires: bzip2

%if 0%{?suse_version}
Requires: libuuid1
BuildRequires: libbz2-devel

%if 0%{?suse_version} >= 1500
BuildRequires: libffi-devel
%endif

%else

BuildRequires: libffi-devel
BuildRequires: bzip2-devel
%if "%{?_vendor}" == "mariner"
Requires: uuid
%else
Requires: libuuid
%endif
%endif


%description
This is OpenResty's python3 package


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/Python-%{version}"; \
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
export LDFLAGS="-L%{ssl_prefix}/lib -L. -L%{_prefix}/lib -Wl,-rpath,%{_prefix}/lib:%{ssl_prefix}/lib"

./configure --prefix="%{_prefix}" --enable-shared --enable-ipv6 \
    --without-ensurepip \
    --libdir="%{_prefix}/lib" \
    --with-openssl=%{ssl_prefix} \
    CFLAGS="-g3 -I%{ssl_prefix}/include" \
    CC='ccache gcc -g3'

make -j`nproc`


%install
make \
    DESTDIR=%{buildroot} \
    INSTALL="install -p" \
    sharedinstall libinstall inclinstall bininstall > /dev/null

find %{buildroot} -type f -print0 | xargs -0 chmod u+w

rm -rf %{buildroot}%{_prefix}/share
( find %{buildroot}%{_prefix}/lib -type d -name 'test' -exec rm -rf "{}" \; || exit 0 )
( find %{buildroot}%{_prefix}/lib -type d -name 'tests' -exec rm -rf "{}" \; || exit 0 )
#( find %{buildroot}%{_prefix}/lib -type d -name '__pycache__' -exec rm -r "{}" \; || exit 0 )

export QA_RPATHS=$[ 0x0002 ]


%files
%defattr(-, root, root)
%attr(0755,root,root) %{_prefix}/bin/*
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
