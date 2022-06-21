Name:           openresty-utils
Version:        0.30
Release:        3%{?dist}
Summary:        OpenResty Utils

Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com

%define prefix          /usr/local/openresty-utils
%define pcre_prefix     /opt/openresty-saas/pcre
%define pcre2_prefix    /opt/openresty-saas/pcre2


Source0:        %{name}-%{version}.tar.gz

AutoReqProv:    no
BuildRequires:  ccache, gcc, make, openresty-saas-pcre-devel
BuildRequires:  openresty-saas-pcre2-devel >= 10.39
BuildRequires:  openresty-libdemangle-devel

Requires:       openresty-saas-pcre
Requires:       openresty-saas-pcre2
Requires:       openresty-libdemangle

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
make -j`nproc` \
    CC='ccache gcc -fdiagnostics-color=always' \
    CFLAGS="-fPIC -O3 -g3 -std=gnu99" \
    CXXFLAGS="-fPIC -std=gnu++11 -g3 -Wall -Werror -O3 -I./src/include -I%{pcre_prefix}/include -I%{pcre2_prefix}/include" \
    LJ_GC_GRAPH_LDFLAGS="-L%{pcre2_prefix}/lib -Wl,-rpath,%{pcre2_prefix}/lib -lpcre2-8" \
    PCRE_PREFIX=%{pcre_prefix}

%install
make install \
    DESTDIR=%{buildroot} PREFIX=%{prefix}
install -d %{buildroot}/usr/bin
ln -sf %{prefix}/bin/resty2 %{buildroot}/usr/bin/resty2

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


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
%{prefix}/bin/fs-fgraph
%{prefix}/bin/resty2
%{prefix}/bin/trie-gen
%{prefix}/lib/libtriegen.so
%{prefix}/bin/lj-gc-graph
%{prefix}/bin/demangle-nm
/usr/bin/resty2


%changelog
* Tue Apr 19 2022 Yichun Zhang (agentzh) 0.30-1
- upgraded openresty-utils to 0.30.
* Tue Dec 14 2021 Yichun Zhang (agentzh) 0.27-1
- upgraded openresty-utils to 0.27.
* Wed Sep 15 2021 LI Geng (ligeng@openresty.com) 0.26-1
- upgraded openresty-utils to 0.26.
* Mon May 24 2021 Yichun Zhang (agentzh) 0.25-1
- upgraded openresty-utils to 0.25.
* Fri Apr 30 2021 LI Geng (ligeng@openresty.com) 0.24-1
- upgraded openresty-utils to 0.24.
* Mon Apr 19 2021 LI Geng (ligeng@openresty.com) 0.23-1
- upgraded openresty-utils to 0.23.
* Tue Apr 6 2021 Yichun Zhang (agentzh) 0.22-1
- upgraded openresty-utils to 0.22.
* Wed Mar 31 2021 Yichun Zhang (agentzh) 0.21-1
- upgraded openresty-utils to 0.21.
* Tue Feb 2 2021 Yichun Zhang (agentzh) 0.20-1
- upgraded openresty-utils to 0.20.
* Tue Feb 2 2021 Yichun Zhang (agentzh) 0.19-1
- upgraded openresty-utils to 0.19.
* Tue Feb 2 2021 Yichun Zhang (agentzh) 0.18-1
- upgraded openresty-utils to 0.18.
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
