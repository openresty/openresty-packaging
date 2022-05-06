Name:           openresty-dw2c
Version:        0.1
Release:        1%{?dist}
Summary:        Tool for converting dwarf to C for OpenResty.

Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com

%define prefix          /usr/local/openresty-dw2c
%define perlcc          /usr/local/openresty-perl/bin/perlcc


Source0:        dw2c-%{version}.tar.gz

AutoReqProv:    no
AutoReq:        no
AutoProv:       no

BuildRequires:  ccache, gcc, make
BuildRequires:  openresty-perl >= 5.24.4
BuildRequires:  openresty-perl-B-C
BuildRequires:  openresty-perl-Cpanel-JSON-XS
BuildRequires:  openresty-perl-devel >= 5.24.4

Requires:   openresty-perl >= 5.24.4
Requires:   openresty-perl-Cpanel-JSON-XS

%description
Tool for converting dwarf to C for OpenResty.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/dw2c-%{version}"; \
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
%setup -q -n dw2c-%{version}

%build
for f in dw2c dw2macros dw2xml find-altlink-files; do \
    %{perlcc} -O2 -o $f ./bin/$f.pl || exit 1; \
done

%install
install -d %{buildroot}%{prefix}/bin
install -m 0755 dw2c dw2xml dw2macros find-altlink-files \
    %{buildroot}%{prefix}/bin

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/bin/dw2c
%{prefix}/bin/dw2macros
%{prefix}/bin/dw2xml
%{prefix}/bin/find-altlink-files


%changelog
* Thu May 05 2022 Johnny Wang <wangjiahao@openresty.com> - 0.1-1
- initial packaging
