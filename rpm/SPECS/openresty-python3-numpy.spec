Name:           openresty-python3-numpy
Version:        1.16.4
Release:        11%{?dist}
Summary:        OpenResty's fork of numpy
Group:          Development/Libraries
License:        BSD
URL:            http://www.numpy.org/
Source0:        https://github.com/numpy/numpy/archive/v%{version}/numpy-%{version}.tar.gz

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


BuildRequires:  lapack-devel
BuildRequires:  gcc
BuildRequires:  openresty-python3-devel >= 3.7.9-12
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  openresty-python3-setuptools >= 39.2.0-3
BuildRequires:  openresty-python3-cython >= 0.28.5-3

Requires:   openresty-python3 >= 3.7.7-2


%description
OpenResty's fork of numpy.
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.
There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/numpy-%{version}"; \
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
%setup -q -n numpy-%{version}


%build
export ATLAS=None
export BLAS=None
export LAPACK=%{_libdir}

PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py build -j`nproc`


%install
export ATLAS=None
export BLAS=None
export LAPACK=%{_libdir}

PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py install --root %{buildroot}

# Remove tests
sed -i 's/from .testing import/# from .testing import/g' %{buildroot}%{py_sitearch}/numpy/__init__.py

rm -rf %{buildroot}%{py_sitearch}/numpy/{compat,core,distutils,f2py,fft,lib,linalg,ma,matrixlib,polynomial,random,testing}/tests

# Remove docs
rm -rf %{buildroot}%{py_sitearch}/numpy/doc

# Remove egg-info
rm -rf %{buildroot}%{py_sitearch}/numpy-%{version}-py%{py_version}.egg-info

# Fix .so permissions
find %{buildroot} -name \*.so -exec chmod 755 {} +

export QA_RPATHS=$[ 0x0002 ]


%files
%defattr(-, root, root)
%{py_sitearch}/numpy/*
%{py_prefix}/bin/f2py*


%clean
rm -rf %{buildroot}


%changelog
