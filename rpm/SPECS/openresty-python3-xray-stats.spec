Name:           openresty-python3-xray-stats
Version:        0.0.3
Release:        1%{?dist}
Summary:        OpenResty XRay Stats Python Library
Group:          Development/Libraries
License:        Proprietary
URL:            https://openresty.com/
Source0:        python-xray-stats-%{version}.tar.gz

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


BuildRequires:  gcc-c++
BuildRequires:  openresty-python3-setuptools >= 39.2.0-3
Requires:   openresty-python3 >= 3.7.9


%description
Python stats library for OpenResty XRay.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/python-xray-stats-%{version}"; \
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
%setup -q -n python-xray-stats-%{version}


%build
make compile %{?_smp_mflags} \
    CXX='g++ -fdiagnostics-color=always' \
    -j1
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py build %{?_smp_mflags}


%install
PATH="%{py_prefix}/bin:$PATH" %{py_bin} setup.py install --root %{buildroot}

# Remove source code
cp %{buildroot}%{py_sitearch}/xray_stats/__pycache__/__init__* %{buildroot}%{py_sitearch}/xray_stats/__init__.pyc
cp %{buildroot}%{py_sitearch}/xray_stats/__pycache__/aggregate* %{buildroot}%{py_sitearch}/xray_stats/aggregate.pyc
rm -f %{buildroot}%{py_sitearch}/xray_stats/*.py

# Remove egg-info
rm -rf %{buildroot}%{py_sitearch}/openresty_python3_xray_stats-%{version}-py%{py_version}.egg-info


%files
%defattr(-, root, root)
%attr(0755,root,root) %{py_sitearch}/xray_stats/libstats.so
%{py_sitearch}/xray_stats/__init__.pyc
%{py_sitearch}/xray_stats/aggregate.pyc
%{py_sitearch}/xray_stats/__pycache__


%clean
rm -rf %{buildroot}


%changelog
* Thu Dec 31 2020 wanghuizzz 0.0.3
- upgraded openresty-python3-xray-stats to 0.0.3.
* Fri Dec 25 2020 wanghuizzz 0.0.1
- initial build for openresty-python3-xray-stats 0.0.1.
