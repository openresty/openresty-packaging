Name:           openresty-maxminddb-utils
Version:        0.0.2
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
OpenResty Maxminddb Utils use to generate maxminddb.
This software is made possible by the mmdbwriter, dns and maxminddb-golang open source project.
https://github.com/maxmind/mmdbwriter/blob/main/LICENSE-MIT
https://github.com/miekg/dns/blob/master/LICENSE
https://github.com/oschwald/maxminddb-golang/blob/main/LICENSE


%global _missing_build_ids_terminate_build 0

# Remove source code from debuginfo package.
%define __debug_install_post \
%{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"\
%{nil}

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
PATH=/opt/go/bin:$PATH make install \
    DESTDIR=%{buildroot} PREFIX=%{prefix}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/bin/qqzeng-converter
%{prefix}/bin/maxminddb-exporter
%{prefix}/bin/maxminddb-add-record
%{prefix}/bin/maxminddb-get-googledns
%config(noreplace) %{prefix}/conf/*


%changelog
* Sat May 08 2021 lijunlong <lijunlong@openresty.com>
- initial packaging
