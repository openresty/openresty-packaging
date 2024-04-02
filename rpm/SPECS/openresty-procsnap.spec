Name:       openresty-procsnap
Version:    3.19.0.1
Release:    1%{?dist}
Summary:    fork and suspend target process

Group: Development/System
License: Proprietary
URL: http://github.com/orinc/criu-plus

%define _missing_doc_files_terminate_build 0

%define procsnap_prefix      %{_usr}/local/openresty-procsnap

Source0: criu-plus-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ccache, cmake, gcc, make
AutoReqProv:        no

Requires: %{name} = %{version}-%{release}

AutoReqProv:        no

%description
Inject code and fork the target process.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/criu-plus-%{version}"; \
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
%setup -q -n criu-plus-%{version}

%build
# NB, we are not using upstream's 'configure'/'make'
# wrapper, instead we use cmake directly to better
# align with Fedora standards
rm -rf build
export CC='ccache gcc -fdiagnostics-color=always'
make -j`nproc` compel/compel-host-bin
make -j`nproc` -C procsnap


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/local/openresty-procsnap/bin
install -c -m 755 procsnap/procsnap $RPM_BUILD_ROOT/usr/local/openresty-procsnap/bin/procsnap

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{procsnap_prefix}/bin/procsnap

%changelog
* Wed Apr 2 2024 Yichun Zhang <yichun@openresty.com> - 3.19.0.1
- Initial build.
