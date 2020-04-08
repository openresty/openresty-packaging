Name:           openresty-firejail
Version:        0.9.62
Release:        1%{?dist}
Summary:        OpenResty's fork of firejail
Group:          Development/Tools
License:        GPLv2+
URL:            https://firejail.wordpress.com/

Source0:        https://github.com/netblue30/firejail/archive/%version.tar.gz

BuildRequires:  gcc make ccache

AutoReqProv: no

%define firejail_prefix %{_usr}/local/%{name}

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/firejail-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%description
OpenResty's fork of firejail.
Firejail is a SUID sandbox program that reduces the risk of security
breaches by restricting the running environment of untrusted applications
using Linux namespaces. It includes a sandbox profile for Mozilla Firefox.

%prep
%setup -q -n firejail-%{version}


%build

%configure \
  --prefix=%{firejail_prefix} \
  --exec_prefix=%{firejail_prefix} \
  --bindir=%{firejail_prefix}/bin \
  --libdir=%{firejail_prefix}/%{_lib} \
  --datarootdir=%{firejail_prefix}/share \
  --mandir=%{firejail_prefix}/man \
  --sysconfdir=%{firejail_prefix}/etc \
  --disable-userns --disable-contrib-install \
  CC='ccache gcc -fdiagnostics-color=always'

make %{?_smp_mflags}


%install

%make_install

# remove useless files
rm -f %{buildroot}/%{firejail_prefix}/bin/firecfg
rm -f %{buildroot}/%{firejail_prefix}/bin/firemon
rm -rf %{buildroot}/%{firejail_prefix}/share/*
rm -rf %{buildroot}/%{firejail_prefix}/man/*

%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%attr(4755, -, -) %{firejail_prefix}/bin/firejail
%{firejail_prefix}/%{_lib}/firejail
%{firejail_prefix}/etc/*


%changelog
* Wed Apr 08 2020 Guisheng Zhou <xlibor@openresty.com>
- initial packaging
