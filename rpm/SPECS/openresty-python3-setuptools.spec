Name:           openresty-python3-setuptools
Version:        75.1.0
Release:        1%{?dist}
Summary:        OpenResty's fork of setuptools
Group:          Development/System
License:        Proprietary
URL:            https://pypi.python.org/pypi/setuptools
BuildArch:      noarch

Source0: https://files.pythonhosted.org/packages/27/b8/f21073fde99492b33ca357876430822e4800cdf522011f18041351dfa74b/setuptools-75.1.0.tar.gz


AutoReqProv: no

%define py_prefix /usr/local/openresty-python3
%define py_bin %{py_prefix}/bin/python3
%define py_lib %{py_prefix}/lib/python3.12
%define py_sitearch %{py_lib}/site-packages

%define __jar_repack 0
%define __brp_mangle_shebangs /usr/bin/true
%define __brp_python_shebangs /usr/bin/true

%global __python %{py_bin}


BuildRequires:  gcc
BuildRequires:  openresty-python3-devel >= 3.12.5-1

Requires:   openresty-python3 >= 3.12.5-1


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
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py build -j`nproc`


%install
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py install --root %{buildroot}


%files
%defattr(-, root, root)
%{py_sitearch}/pkg_resources/
%{py_sitearch}/setuptools*/
%{py_sitearch}/_distutils_hack
%{py_sitearch}/distutils-precedence.pth

%clean
rm -rf %{buildroot}


%changelog
