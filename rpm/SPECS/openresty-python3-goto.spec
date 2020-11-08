Name:           openresty-python3-goto
Version:        1.2.1
Release:        2%{?dist}
Summary:        OpenResty's fork of python goto library
Group:          Development/Libraries
License:        Public Domain
URL:            https://github.com/snoack/python-goto
Source0:        python-goto-plus-%{version}.tar.gz
BuildArch:      noarch

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

%global debug_package %{nil}


%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


BuildRequires:  openresty-python3-devel >= 3.7.9-3
BuildRequires:  openresty-python3-setuptools >= 39.2.0-3

Requires:   openresty-python3 >= 3.7.9-3


%description
OpenResty's fork of python goto.
A function decorator, that rewrites the bytecode, to enable goto in Python.


%prep
%setup -q -n python-goto-plus-%{version}


%build
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py build %{?_smp_mflags}


%install
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py install --root %{buildroot}


# Remove egg-info
rm -rf %{buildroot}%{py_sitearch}/goto_statement-%{version}-py%{py_version}.egg-info


export QA_RPATHS=$[ 0x0002 ]


%files
%defattr(-, root, root)
%{py_sitearch}/*


%clean
rm -rf %{buildroot}


%changelog
