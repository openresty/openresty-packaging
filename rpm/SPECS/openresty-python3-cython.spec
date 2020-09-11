Name:           openresty-python3-cython
Version:        0.28.5
Release:        2%{?dist}
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

%global __python %{py_bin}


# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/cython-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires:  gcc
BuildRequires:  openresty-python3-devel

Requires:   openresty-python3


%description
OpenResty's fork of cython.
This is a development version of Pyrex, a language for writing Python extension modules.


%prep
%setup -q -n cython-%{version}


%build
PYTHONPATH="%{py_lib}:%{py_sitearch}:%{buildroot}%{py_lib}:%{buildroot}%{py_sitearch}" PATH=%{buildroot}%{py_prefix}/bin:%{_bindir}:$PATH %{py_bin} setup.py build %{?_smp_mflags}


%install
PYTHONPATH="%{py_lib}:%{py_sitearch}:%{buildroot}%{py_lib}:%{buildroot}%{py_sitearch}" PATH=%{buildroot}%{py_prefix}/bin:%{_bindir}:$PATH %{py_bin} setup.py install --root %{buildroot}

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
