Name:           openresty-python3-cython
Version:        0.28.5
Release:        6%{?dist}
Summary:        OpenResty's fork of Cython
Group:          Development/System
License:        ASL
URL:            http://www.cython.org

Source0:        https://github.com/cython/cython/archive/%{version}/Cython-%{version}.tar.gz

AutoReqProv: no

%define py_prefix /usr/local/openresty-python3
%define py_bin %{py_prefix}/bin/python3
%define py_lib %{py_prefix}/lib/python3.7
%define py_sitearch %{py_lib}/site-packages
%define py_version 3.7

%define __jar_repack 0
%define __brp_mangle_shebangs /usr/bin/true
%define __brp_python_shebangs /usr/bin/true

%global __python %{py_bin}


BuildRequires:  gcc
BuildRequires:  openresty-python3-devel >= 3.7.7-2

Requires:   openresty-python3 >= 3.7.7-2


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
%{py_sitearch}/__pycache__/cython.cpython-37*.py*


%clean
rm -rf %{buildroot}


%changelog
