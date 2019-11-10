Name:           openresty-utils
Version:        0.02
Release:        1%{?dist}
Summary:        OpenResty Utils

Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com

%define prefix  %{_usr}/local/openresty-utils

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{name}-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

Source0:        %{name}-%{version}.tar.gz

BuildRequires:  ccache, gcc, make

%description
OpenResty Utils


%prep
%setup -q -n %{name}-%{version}

%build
make %{?_smp_mflags} \
    CC='ccache gcc -fdiagnostics-color=always' \
    CFLAGS="-O3 -g3"

%install
make install \
    DESTDIR=%{buildroot} PREFIX=%{prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/bin/crc32_fast


%changelog
* Sun Nov 10 2019 Johnny Wang <wangjiahao@openresty.com>
- initial packaging
