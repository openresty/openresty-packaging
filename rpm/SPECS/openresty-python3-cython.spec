Name:           openresty-python3-cython
Version:        3.0.11
Release:        3%{?dist}
Summary:        OpenResty's fork of Cython
Group:          Development/System
License:        Proprietary
URL:            http://www.cython.org

Source0:        https://github.com/cython/cython/releases/download/%{version}-1/cython-%{version}.tar.gz
AutoReqProv: no

%define py_prefix /usr/local/openresty-python3
%define py_bin %{py_prefix}/bin/python3
%define py_lib %{py_prefix}/lib/python3.12
%define py_sitearch %{py_lib}/site-packages
%define py_version 3.12

%define __jar_repack 0
%define __brp_mangle_shebangs /usr/bin/true
%define __brp_python_shebangs /usr/bin/true

%global __python %{py_bin}


BuildRequires:  gcc
BuildRequires:  openresty-python3-devel >= 3.12.5-1
BuildRequires:  openresty-python3-setuptools >= 75.1.0

Requires:   openresty-python3 >= 3.12.5-1


%description
OpenResty's fork of cython.
This is a development version of Pyrex, a language for writing Python extension modules.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/cython-%{version}"; \
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
%setup -q -n cython-%{version}


%build
find . -type f -name "*.py" | xargs sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python3|'
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py build -j`nproc`


%install
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py install --root %{buildroot}

# Remove egg-info
rm -rf %{buildroot}%{py_sitearch}/Cython-%{version}-py%{py_version}.egg-info

export QA_RPATHS=$[ 0x0002 ]


%files
%defattr(-, root, root)
%{py_prefix}/bin/cython
%{py_prefix}/bin/cythonize
%{py_prefix}/bin/cygdb
%{py_sitearch}/cython.*
%{py_sitearch}/Cython/
%{py_sitearch}/pyximport/
%{py_sitearch}/__pycache__/cython.cpython-312*.py*


%clean
rm -rf %{buildroot}


%changelog
