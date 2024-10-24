Name:           openresty-python3-numpy
Version:        2.1.1
Release:        4%{?dist}
Summary:        OpenResty's fork of numpy
Group:          Development/Libraries
License:        Proprietary
URL:            http://www.numpy.org/
Source0:        https://github.com/numpy/numpy/releases/download/v%{version}/numpy-%{version}.tar.gz

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


BuildRequires:  lapack-devel
BuildRequires:  gcc
BuildRequires:  openresty-python3-devel >= 3.12.5-1
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  openresty-python3-setuptools >= 72.2.0-1
BuildRequires:  openresty-python3-cython >= 3.0.11-7

Requires:   openresty-python3 >= 3.12.5-1


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

export PATH=$HOME/.local/bin:%{py_prefix}/bin:$PATH
rm -fr $HOME/.local/bin/cython
rm -fr $HOME/.local/bin/cygdb
rm -fr $HOME/.local/bin/cythonize
#if [ -z "$(command -v $HOME/.local/bin/pip3)" ]; then
#fi
wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

#if [ -z "$(command -v $HOME/.local/bin/meson)" ]; then
pip3 install --user meson
#fi

#if [ -z "$(command -v $HOME/.local/bin/spin)" ]; then
pip3 install --user spin
#fi

#if [ -z "$(command -v $HOME/.local/bin/ninja)" ]; then
pip3 install --user ninja
#fi
spin build  -j`nproc` -- --prefix=%{py_prefix}

%install
export ATLAS=None
export BLAS=None
export LAPACK=%{_libdir}

rm -rf build-install/%{py_sitearch}/numpy/{compat,core,_core,distutils,f2py,fft,lib,linalg,ma,matrixlib,polynomial,random,typing,testing,_pyinstaller}/tests
rm -rf build-install/%{py_sitearch}/numpy/tests

install -d %{buildroot}

cp -ra build-install/* %{buildroot}/

export QA_RPATHS=$[ 0x0002 ]


%files
%defattr(-, root, root)
%{py_sitearch}/numpy/*


%clean
rm -rf %{buildroot}


%changelog
