Name:           openresty-utils
Version:        0.17
Release:        2%{?dist}
Summary:        OpenResty Utils

Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com

%define prefix  %{_usr}/local/openresty-utils


Source0:        %{name}-%{version}.tar.gz

BuildRequires:  ccache, gcc, make

%description
OpenResty Utils


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openresty-utils-%{version}"; \
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
%setup -q -n %{name}-%{version}

%build
make %{?_smp_mflags} \
    CC='ccache gcc -fdiagnostics-color=always' \
    CFLAGS="-O3 -g3 -std=gnu99"

%install
make install \
    DESTDIR=%{buildroot} PREFIX=%{prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/bin/crc32_fast
%{prefix}/bin/start-stop-daemon
%{prefix}/bin/flush-page-cache
%{prefix}/bin/read-pagemap
%{prefix}/bin/extract-vmlinux
%{prefix}/bin/mincore
%{prefix}/bin/read-umem
%{prefix}/bin/shm-warmup
%{prefix}/bin/shared-pages
%{prefix}/bin/read-kern-bid


%changelog
* Sun Dec 6 2020 Yichun Zhang (agentzh) 0.17-1
- upgraded openresty-utils to 0.17.
* Fri Jul 31 2020 Yichun Zhang (agentzh) 0.16-1
- upgraded openresty-utils to 0.16.
* Sun Jul 26 2020 Yichun Zhang (agentzh) 0.15-1
- upgraded openresty-utils to 0.15.
* Wed May 20 2020 Yichun Zhang (agentzh) 0.14-1
- upgraded openresty-utils to 0.14.
* Sun May 10 2020 Yichun Zhang (agentzh) 0.13-1
- upgraded openresty-utils to 0.13.
* Sun May 10 2020 Yichun Zhang (agentzh) 0.12-1
- upgraded openresty-utils to 0.12.
* Sun May 10 2020 Yichun Zhang (agentzh) 0.11-1
- upgraded openresty-utils to 0.11.
* Sat Apr 25 2020 Yichun Zhang (agentzh) 0.10-1
- upgraded openresty-utils to 0.10.
* Sat Apr 25 2020 Yichun Zhang (agentzh) 0.09-1
- upgraded openresty-utils to 0.09.
* Tue Apr 21 2020 Yichun Zhang (agentzh) 0.08-1
- upgraded openresty-utils to 0.08.
* Sun Feb 23 2020 Yichun Zhang (agentzh) 0.04-1
- upgraded openresty-utils to 0.04.
* Sun Nov 10 2019 Johnny Wang <wangjiahao@openresty.com>
- initial packaging
