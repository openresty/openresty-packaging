Name:           openresty-maxminddb-utils
Version:        0.0.1
Release:        1%{?dist}
Summary:        OpenResty Maxminddb Utils

Group:          Development/Tools
License:        Proprietary
URL:            https://www.openresty.com

%define prefix  %{_usr}/local/openresty-maxminddb-utils


Source0:        maxminddb-utils-%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  make

%description
OpenResty Maxminddb Utils

%global _missing_build_ids_terminate_build 0

%if 0%{?suse_version}

%debug_package

%else
# Remove source code from debuginfo package.
%define __debug_install_post \
%{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"\
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
%setup -q -n maxminddb-utils-%{version}

%build
PATH=/opt/go/bin:$PATH make -j`nproc`

%install
make install \
    DESTDIR=%{buildroot} PREFIX=%{prefix}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/bin/maxminddb-exporter
%{prefix}/bin/qqzeng-converter
%config(noreplace) %{prefix}/conf/*


%changelog
* Sat May 08 2021 lijunlong <lijunlong@openresty.com>
- initial packaging
