Name:           openresty-minifiers
Version:        0.0.2
Release:        1%{?dist}
Summary:        OpenResty Inc's minifiers for CSS/HTML/JS/etc

Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com

%define prefix          /usr/local/openresty-minifiers

Source0:        or-minifiers-%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  ccache, gcc, make

%description
OpenResty Inc's minifiers for CSS/HTML/JS/etc


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/or-minifiers-%{version}"; \
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
%setup -q -n or-minifiers-%{version}

%build
free=`free -m|grep -E '^Mem'|head -n1|awk '{print $NF}'`
ncpus=`nproc`
max_jobs=$(( $free / 4096 ))
# echo "max jobs: $max_jobs"
if [ "$max_jobs" -gt "$ncpus" ]; then
    max_jobs=$ncpus
fi
make -j$max_jobs \
    CC='ccache gcc -fdiagnostics-color=always'

%install
install -d %{buildroot}%{prefix}/lib
install -d %{buildroot}%{prefix}/tpls
install min-css.so min-html.so min-js.so \
    %{buildroot}%{prefix}/lib
install -m 644 tpls/* %{buildroot}%{prefix}/tpls

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{prefix}
%dir %{prefix}/lib
%defattr(-,root,root,-)
%{prefix}/lib/min-css.so
%{prefix}/lib/min-html.so
%{prefix}/lib/min-js.so
%{prefix}/tpls/*


%changelog
* Sun May 12 2024 Yichun Zhang (agentzh) 0.0.2-1
- upgraded or-minifiers to 0.0.2.
* Wed May 08 2024 Johnny Wang <wangjiahao@openresty.com>
- initial packaging
