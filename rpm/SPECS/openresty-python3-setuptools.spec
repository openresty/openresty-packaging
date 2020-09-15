Name:           openresty-python3-setuptools
Version:        39.2.0
Release:        4%{?dist}
Summary:        OpenResty's fork of setuptools
Group:          Development/System
License:        MIT
URL:            https://pypi.python.org/pypi/setuptools

Source0:        https://files.pythonhosted.org/packages/source/s/setuptools/setuptools-%{version}.zip

AutoReqProv: no

%define py_prefix /usr/local/openresty-python3
%define py_bin %{py_prefix}/bin/python3
%define py_lib %{py_prefix}/lib/python3.7
%define py_sitearch %{py_lib}/site-packages

%define __jar_repack 0
%define __brp_mangle_shebangs /usr/bin/true
%define __brp_python_shebangs /usr/bin/true

%global __python %{py_bin}
%global debug_package %{nil}


%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires:  gcc
BuildRequires:  openresty-python3-devel >= 3.7.7-2

Requires:   openresty-python3 >= 3.7.7-2


%description
OpenResty's fork of setuptools.
Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.


%prep
%setup -q -n setuptools-%{version}


%build
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py build %{?_smp_mflags}


%install
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py install --root %{buildroot}


%files
%defattr(-, root, root)
%{py_sitearch}/easy_install.*
%{py_sitearch}/pkg_resources/
%{py_sitearch}/setuptools*/
%{py_sitearch}/__pycache__/*
%{py_prefix}/bin/easy_install
%{py_prefix}/bin/easy_install-3.*


%clean
rm -rf %{buildroot}


%changelog
