Name:           openresty-stap
Version:        4.9.0.23
Release:        1%{?dist}
Summary:        OpenResty's fork of SystemTap
Group:          Development/System
License:        GPLv2+
URL:            http://sourceware.org/systemtap/
Provides:       openresty-stap

Source0:        systemtap-plus-%{version}.tar.gz

AutoReqProv:    no

%global _python_bytecompile_extra 0

%define _rpmmacrodir %{_rpmconfigdir}/macros.d

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%define stap_prefix %{_usr}/local/%{name}

%define eu_prefix %{_usr}/local/openresty-elfutils


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ccache, gcc-c++, openresty-python3 >= 3.7.9
#BuildRequires: perl-JSON-MaybeXS
BuildRequires: openresty-perl, openresty-perl-Cpanel-JSON-XS
BuildRequires: gettext-devel
BuildRequires: m4, sed
BuildRequires: zlib-devel
BuildRequires: xz-devel

%if 0%{?suse_version}
BuildRequires: libbz2-devel
%else
BuildRequires: bzip2-devel
%endif

BuildRequires: openresty-elfutils-devel >= 0.177.12-1

%if 0%{?suse_version}
Requires: libbz2-1
%else
Requires: bzip2-libs
%endif

%if 0%{?suse_version}
Requires: liblzma5
%else
Requires: xz-libs
%endif

Requires: zlib
Requires: make, openresty-perl, openresty-perl-Cpanel-JSON-XS
Requires: openresty-stap-runtime = %{version}-%{release}
Requires: openresty-elfutils >= 0.177.12-1

%undefine __brp_mangle_shebangs

%description
OpenResty's fork of SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system. The base systemtap package contains/requires
the components needed to locally develop and execute systemtap scripts.

# ------------------------------------------------------------------------


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/systemtap-plus-%{version}"; \
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


%package runtime
Summary: Programmable system-wide instrumentation system - runtime (OpenResty's fork of SystemTap)
Group: Development/System
License: GPLv2+
URL: http://sourceware.org/systemtap/

%if 0%{?suse_version}
Requires(pre): shadow
%else
Requires(pre): shadow-utils
%endif

%description runtime
OpenResty's fork of SystemTap runtime contains the components needed to execute
a systemtap script that was already compiled into a module
using a local or remote systemtap-devel installation.


%package sdt-devel
Summary: Static probe support tools (OpenResty's fork of SystemTap)
Group: Development/System
License: GPLv2+ and Public Domain
AutoReqProv:    no
URL: http://sourceware.org/systemtap/
Requires: openresty-python3


%description sdt-devel
OpenResty's fork of SystemTap sdt-devel includes the <sys/sdt.h> header file
used for static instrumentation compiled into userspace programs and libraries,
along with the optional dtrace-compatibility preprocessor to process related
.d files into tracing-macro-laden .h headers.


%package tests
Summary: Test suite for OpenResty's SystemTap+
Group: Development/System
License: GPLv2+ and Public Domain
AutoReqProv:    no
URL: http://sourceware.org/systemtap/
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description tests
Test suite for OpenResty's SystemTap+


%prep
%setup -q -n systemtap-plus-%{version}


%build
cd tapset/
arch="%{_arch}"
if [[ "%{_arch}" == "aarch64" ]]; then
    arch="arm64"
fi
/usr/local/openresty-perl/bin/perl ../util/parse-tapset-deps.pl $arch/*.stp *.{stp,stpm} linux/$arch/*.stp linux/*.{stp,stpm}
cd ..

export PATH=/usr/local/openresty-python3/bin:$PATH

ccache gcc -v
ccache g++ -v

./configure \
        --prefix=%{stap_prefix} \
        --libexecdir="%{stap_prefix}/libexec" \
        --disable-docs --disable-publican \
        --with-python3 \
        --without-nss \
        --without-openssl \
        --without-avahi \
        --without-bpf \
        --without-rpm \
        --without-dyninst \
        --without-python2-probes \
        --without-python3-probes \
        --disable-refdocs \
        CC='ccache gcc -fdiagnostics-color=always' \
        CXX='ccache g++ -fdiagnostics-color=always' \
        CFLAGS='-I%{eu_prefix}/include -g -O2 -Wno-error=implicit-fallthrough' \
        CXXFLAGS='-I%{eu_prefix}/include -g -O2 -Wno-error=implicit-fallthrough' \
        LDFLAGS='-L%{eu_prefix}/lib -Wl,-rpath,%{eu_prefix}/lib'

make -j`nproc` V=1

%install

mkdir -p %{buildroot}%{stap_prefix}/share/systemtap/
install -c -m 644 tapset/tapset-deps.data %{buildroot}%{stap_prefix}/share/systemtap/
rm tapset/tapset-deps.data
mkdir -p %{buildroot}%{stap_prefix}/bin/
install -c -m 755 util/parse-stp-deps.pl %{buildroot}%{stap_prefix}/bin/

export PATH=/usr/local/openresty-python3/bin:$PATH
make install DESTDIR=%{buildroot}

sed -i 's/^#!.*python*/#!\/usr\/local\/openresty-python3\/bin\/python3/' \
    %{buildroot}%{stap_prefix}/bin/dtrace

# Because "make install" may install staprun with whatever mode, the
# post-processing programs rpmbuild runs won't be able to read it.
# So, we change permissions so that they can read it.  We'll set the
# permissions back to 04110 in the %files section below.
chmod 755 %{buildroot}%{stap_prefix}/bin/staprun

#install the useful stap-prep script
install -c -m 755 stap-prep %{buildroot}%{stap_prefix}/bin/stap-prep

rm t/data/bug-addr2name/libssl.so.1.1
cp -r t %{buildroot}%{stap_prefix}/

#install -D -m 644 macros.systemtap %{buildroot}%{_rpmmacrodir}/macros.systemtap

# remove useless files
rm -rf %{buildroot}%{stap_prefix}/share/man
rm -rf %{buildroot}%{stap_prefix}/share/systemtap/examples
rm -rf %{buildroot}%{stap_prefix}/share/locale
rm -rf %{buildroot}%{stap_prefix}/lib64/python2.7
rm -f %{buildroot}%{stap_prefix}/bin/stap-server
rm -f %{buildroot}%{stap_prefix}/bin/stapbpf
rm -f %{buildroot}%{stap_prefix}/bin/stap-prep
rm -f %{buildroot}%{stap_prefix}/bin/stap-report
rm -f %{buildroot}%{stap_prefix}/bin/stapsh
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-env
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-gen-cert
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-serverd
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-sign-module
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-start-server
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/stap-stop-server
rm -f %{buildroot}%{stap_prefix}/libexec/systemtap/python/stap-resolve-module-function.py*
rm -rf %{buildroot}%{stap_prefix}/share/systemtap/interactive-notebook/

rm -f %{buildroot}%{stap_prefix}/bin/stap-jupyter-container \
   %{buildroot}%{stap_prefix}/bin/stap-jupyter-install \
   %{buildroot}%{stap_prefix}/bin/stap-profile-annotate \
   %{buildroot}%{stap_prefix}/libexec/systemtap/HelperSDT.jar \
   %{buildroot}%{stap_prefix}/libexec/systemtap/libHelperSDT.so \
   %{buildroot}%{stap_prefix}/libexec/systemtap/stapbm

export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%{stap_prefix}/bin/stap
%{stap_prefix}/bin/parse-stp-deps.pl
%dir %{stap_prefix}/share/systemtap
%{stap_prefix}/share/systemtap/runtime
%{stap_prefix}/share/systemtap/tapset
%{stap_prefix}/share/systemtap/tapset-deps.data


%files runtime
%defattr(-,root,root)
%attr(4110,root,stapusr) %{stap_prefix}/bin/staprun
%{stap_prefix}/bin/stap-merge
%dir %{stap_prefix}/libexec/systemtap
%{stap_prefix}/libexec/systemtap/stapio


%files sdt-devel
%defattr(-,root,root)
%{stap_prefix}/bin/dtrace
%{stap_prefix}/include/sys/sdt.h
%{stap_prefix}/include/sys/sdt-config.h


%files tests
%defattr(-,root,root)
%dir %{stap_prefix}/t
%{stap_prefix}/t/*

# ------------------------------------------------------------------------

%changelog
* Mon Feb 26 2024 Yichun Zhang (agentzh) 4.9.0.23-1
- upgraded openresty-stap to 4.9.0.23.
* Wed Jan 3 2024 Yichun Zhang (agentzh) 4.9.0.22-1
- upgraded openresty-stap to 4.9.0.22.
* Sat Dec 30 2023 Yichun Zhang (agentzh) 4.9.0.21-1
- upgraded openresty-stap to 4.9.0.21.
* Thu Dec 21 2023 Yichun Zhang (agentzh) 4.9.0.20-1
- upgraded openresty-stap to 4.9.0.20.
* Sun Dec 10 2023 Yichun Zhang (agentzh) 4.9.0.19-1
- upgraded openresty-stap to 4.9.0.19.
* Fri Dec 1 2023 Yichun Zhang (agentzh) 4.9.0.18-1
- upgraded openresty-stap to 4.9.0.18.
* Mon Nov 13 2023 Yichun Zhang (agentzh) 4.9.0.17-1
- upgraded openresty-stap to 4.9.0.17.
* Mon Nov 13 2023 Yichun Zhang (agentzh) 4.9.0.16-1
- upgraded openresty-stap to 4.9.0.16.
* Mon Nov 13 2023 Yichun Zhang (agentzh) 4.9.0.15-1
- upgraded openresty-stap to 4.9.0.15.
* Thu Nov 9 2023 Yichun Zhang (agentzh) 4.9.0.14-1
- upgraded openresty-stap to 4.9.0.14.
* Thu Nov 2 2023 Yichun Zhang (agentzh) 4.9.0.13-1
- upgraded openresty-stap to 4.9.0.13.
* Tue Oct 17 2023 Yichun Zhang (agentzh) 4.9.0.12-1
- upgraded openresty-stap to 4.9.0.12.
* Wed Aug 30 2023 Yichun Zhang (agentzh) 4.9.0.10-1
- upgraded openresty-stap to 4.9.0.10.
* Thu Aug 24 2023 Yichun Zhang (agentzh) 4.9.0.9-1
- upgraded openresty-stap to 4.9.0.9.
* Tue Jul 18 2023 Yichun Zhang (agentzh) 4.9.0.8-1
- upgraded openresty-stap to 4.9.0.8.
* Mon Jun 26 2023 Yichun Zhang (agentzh) 4.9.0.7-1
- upgraded openresty-stap to 4.9.0.7.
* Thu Jun 8 2023 Yichun Zhang (agentzh) 4.9.0.6-1
- upgraded openresty-stap to 4.9.0.6.
* Thu May 25 2023 Yichun Zhang (agentzh) 4.9.0.4-1
- upgraded openresty-stap to 4.9.0.4.
* Tue May 23 2023 Yichun Zhang (agentzh) 4.9.0.3-1
- upgraded openresty-stap to 4.9.0.3.
* Mon May 1 2023 Yichun Zhang (agentzh) 4.9.0.2-1
- upgraded openresty-stap to 4.9.0.2.
* Thu Apr 27 2023 Yichun Zhang (agentzh) 4.9.0.1-1
- upgraded openresty-stap to 4.9.0.1.
* Mon Jan 9 2023 Yichun Zhang (agentzh) 4.7.0.26-1
- upgraded openresty-stap to 4.7.0.26.
* Tue Nov 22 2022 Yichun Zhang (agentzh) 4.7.0.25-1
- upgraded openresty-stap to 4.7.0.25.
* Wed Nov 9 2022 Yichun Zhang (agentzh) 4.7.0.24-1
- upgraded openresty-stap to 4.7.0.24.
* Sun Nov 6 2022 Yichun Zhang (agentzh) 4.7.0.23-1
- upgraded openresty-stap to 4.7.0.23.
* Wed Nov 2 2022 Yichun Zhang (agentzh) 4.7.0.22-1
- upgraded openresty-stap to 4.7.0.22.
* Wed Nov 2 2022 Yichun Zhang (agentzh) 4.7.0.21-1
- upgraded openresty-stap to 4.7.0.21.
* Mon Oct 10 2022 Yichun Zhang (agentzh) 4.7.0.19-1
- upgraded openresty-stap to 4.7.0.19.
* Wed Sep 28 2022 Yichun Zhang (agentzh) 4.7.0.18-1
- upgraded openresty-stap to 4.7.0.18.
* Tue Sep 27 2022 Yichun Zhang (agentzh) 4.7.0.17-1
- upgraded openresty-stap to 4.7.0.17.
* Tue Sep 27 2022 Yichun Zhang (agentzh) 4.7.0.16-1
- upgraded openresty-stap to 4.7.0.16.
* Mon Sep 26 2022 Yichun Zhang (agentzh) 4.7.0.15-1
- upgraded openresty-stap to 4.7.0.15.
* Sun Sep 25 2022 Yichun Zhang (agentzh) 4.7.0.14-1
- upgraded openresty-stap to 4.7.0.14.
* Thu Sep 22 2022 Yichun Zhang (agentzh) 4.7.0.13-1
- upgraded openresty-stap to 4.7.0.13.
* Wed Sep 21 2022 Yichun Zhang (agentzh) 4.7.0.12-1
- upgraded openresty-stap to 4.7.0.12.
* Sat Sep 10 2022 Yichun Zhang (agentzh) 4.7.0.11-1
- upgraded openresty-stap to 4.7.0.11.
* Sun Sep 4 2022 Yichun Zhang (agentzh) 4.7.0.10-1
- upgraded openresty-stap to 4.7.0.10.
* Sat Sep 3 2022 Yichun Zhang (agentzh) 4.7.0.9-1
- upgraded openresty-stap to 4.7.0.9.
* Wed Aug 31 2022 Yichun Zhang (agentzh) 4.7.0.8-1
- upgraded openresty-stap to 4.7.0.8.
* Mon Jun 27 2022 Yichun Zhang (agentzh) 4.7.0.7-1
- upgraded openresty-stap to 4.7.0.7.
* Fri Jun 24 2022 Yichun Zhang (agentzh) 4.7.0.6-1
- upgraded openresty-stap to 4.7.0.6.
* Wed Apr 27 2022 Yichun Zhang (agentzh) 4.7.0.5-1
- upgraded openresty-stap to 4.7.0.5.
* Wed Apr 13 2022 Yichun Zhang (agentzh) 4.7.0.4-1
- upgraded openresty-stap to 4.7.0.4.
* Wed Apr 13 2022 Yichun Zhang (agentzh) 4.7.0.3-1
- upgraded openresty-stap to 4.7.0.3.
* Mon Apr 4 2022 Yichun Zhang (agentzh) 4.7.0.2-1
- upgraded openresty-stap to 4.7.0.2.
* Wed Mar 23 2022 Yichun Zhang (agentzh) 4.7.0.1-1
- upgraded openresty-stap to 4.7.0.1.
* Thu Oct 28 2021 Yichun Zhang (agentzh) 4.6.0.8-1
- upgraded openresty-stap to 4.6.0.8.
* Tue Oct 5 2021 Yichun Zhang (agentzh) 4.6.0.7-1
- upgraded openresty-stap to 4.6.0.7.
* Sun Sep 19 2021 Yichun Zhang (agentzh) 4.6.0.6-1
- upgraded openresty-stap to 4.6.0.6.
* Sun Aug 29 2021 Yichun Zhang (agentzh) 4.6.0.5-1
- upgraded openresty-stap to 4.6.0.5.
* Wed Aug 11 2021 Yichun Zhang (agentzh) 4.6.0.4-1
- upgraded openresty-stap to 4.6.0.4.
* Sun Jul 25 2021 Yichun Zhang (agentzh) 4.6.0.3-1
- upgraded openresty-stap to 4.6.0.3.
* Thu Jul 15 2021 Yichun Zhang (agentzh) 4.6.0.2-1
- upgraded openresty-stap to 4.6.0.2.
* Wed Jun 30 2021 Yichun Zhang (agentzh) 4.6.0.1-1
- upgraded openresty-stap to 4.6.0.1.
* Tue May 18 2021 Yichun Zhang (agentzh) 4.5.0.18-1
- upgraded openresty-stap to 4.5.0.18.
* Wed Apr 21 2021 Yichun Zhang (agentzh) 4.5.0.17-1
- upgraded openresty-stap to 4.5.0.17.
* Fri Feb 5 2021 Yichun Zhang (agentzh) 4.5.0.16-1
- upgraded openresty-stap to 4.5.0.16.
* Wed Feb 3 2021 Yichun Zhang (agentzh) 4.5.0.15-1
- upgraded openresty-stap to 4.5.0.15.
* Fri Jan 29 2021 Yichun Zhang (agentzh) 4.5.0.13-1
- upgraded openresty-stap to 4.5.0.13.
* Thu Jan 28 2021 Yichun Zhang (agentzh) 4.5.0.12-1
- upgraded openresty-stap to 4.5.0.12.
* Fri Jan 22 2021 Yichun Zhang (agentzh) 4.5.0.11-1
- upgraded openresty-stap to 4.5.0.11.
* Wed Jan 20 2021 Yichun Zhang (agentzh) 4.5.0.10-1
- upgraded openresty-stap to 4.5.0.10.
* Mon Jan 18 2021 Yichun Zhang (agentzh) 4.5.0.9-1
- upgraded openresty-stap to 4.5.0.9.
* Fri Jan 8 2021 Yichun Zhang (agentzh) 4.5.0.8-1
- upgraded openresty-stap to 4.5.0.8.
* Mon Jan 4 2021 Yichun Zhang (agentzh) 4.5.0.7-1
- upgraded openresty-stap to 4.5.0.7.
* Wed Dec 30 2020 Yichun Zhang (agentzh) 4.5.0.6-1
- upgraded openresty-stap to 4.5.0.6.
* Thu Dec 24 2020 Yichun Zhang (agentzh) 4.5.0.5-1
- upgraded openresty-stap to 4.5.0.5.
* Thu Dec 24 2020 Yichun Zhang (agentzh) 4.5.0.4-1
- upgraded openresty-stap to 4.5.0.4.
* Wed Dec 23 2020 Yichun Zhang (agentzh) 4.5.0.3-1
- upgraded openresty-stap to 4.5.0.3.
* Mon Dec 21 2020 Yichun Zhang (agentzh) 4.5.0.2-1
- upgraded openresty-stap to 4.5.0.2.
* Wed Dec 16 2020 Yichun Zhang (agentzh) 4.5.0.1-1
- upgraded openresty-stap to 4.5.0.1.
* Tue Dec 8 2020 Yichun Zhang (agentzh) 4.3.0.48-1
- upgraded openresty-stap to 4.3.0.48.
* Wed Nov 25 2020 Yichun Zhang (agentzh) 4.3.0.47-1
- upgraded openresty-stap to 4.3.0.47.
* Thu Nov 12 2020 Yichun Zhang (agentzh) 4.3.0.46-1
- upgraded openresty-stap to 4.3.0.46.
* Thu Nov 5 2020 Yichun Zhang (agentzh) 4.3.0.45-1
- upgraded openresty-stap to 4.3.0.45.
* Thu Oct 29 2020 Yichun Zhang (agentzh) 4.3.0.44-1
- upgraded openresty-stap to 4.3.0.44.
* Tue Oct 27 2020 Yichun Zhang (agentzh) 4.3.0.43-1
- upgraded openresty-stap to 4.3.0.43.
* Sat Oct 24 2020 Yichun Zhang (agentzh) 4.3.0.41-1
- upgraded openresty-stap to 4.3.0.41.
* Wed Oct 21 2020 Yichun Zhang (agentzh) 4.3.0.40-1
- upgraded openresty-stap to 4.3.0.40.
* Thu Oct 1 2020 Yichun Zhang (agentzh) 4.3.0.39-1
- upgraded openresty-stap to 4.3.0.39.
* Wed Sep 30 2020 Yichun Zhang (agentzh) 4.3.0.38-1
- upgraded openresty-stap to 4.3.0.38.
* Mon Sep 28 2020 Yichun Zhang (agentzh) 4.3.0.37-1
- upgraded openresty-stap to 4.3.0.37.
* Wed Sep 23 2020 Yichun Zhang (agentzh) 4.3.0.36-1
- upgraded openresty-stap to 4.3.0.36.
* Sun Sep 6 2020 Yichun Zhang (agentzh) 4.3.0.35-1
- upgraded openresty-stap to 4.3.0.35.
* Mon Aug 17 2020 Yichun Zhang (agentzh) 4.3.0.34-1
- upgraded openresty-stap to 4.3.0.34.
* Fri Aug 14 2020 Yichun Zhang (agentzh) 4.3.0.33-1
- upgraded openresty-stap to 4.3.0.33.
* Sat Aug 1 2020 Yichun Zhang (agentzh) 4.3.0.32-1
- upgraded openresty-stap to 4.3.0.32.
* Tue Jul 28 2020 Yichun Zhang (agentzh) 4.3.0.31-1
- upgraded openresty-stap to 4.3.0.31.
* Sun Jun 21 2020 Yichun Zhang (agentzh) 4.3.0.30-1
- upgraded openresty-stap to 4.3.0.30.
* Sat Jun 13 2020 Yichun Zhang (agentzh) 4.3.0.29-1
- upgraded openresty-stap to 4.3.0.29.
* Tue Jun 9 2020 Yichun Zhang (agentzh) 4.3.0.28-1
- upgraded openresty-stap to 4.3.0.28.
* Tue Jun 9 2020 Yichun Zhang (agentzh) 4.3.0.27-1
- upgraded openresty-stap to 4.3.0.27.
* Mon Jun 8 2020 Yichun Zhang (agentzh) 4.3.0.26-1
- upgraded openresty-stap to 4.3.0.26.
* Sun Jun 7 2020 Yichun Zhang (agentzh) 4.3.0.25-1
- upgraded openresty-stap to 4.3.0.25.
* Sat Jun 6 2020 Yichun Zhang (agentzh) 4.3.0.24-1
- upgraded openresty-stap to 4.3.0.24.
* Mon May 11 2020 Yichun Zhang (agentzh) 4.3.0.23-1
- upgraded openresty-stap to 4.3.0.23.
* Fri May 8 2020 Yichun Zhang (agentzh) 4.3.0.22-1
- upgraded openresty-stap to 4.3.0.22.
* Fri May 8 2020 Yichun Zhang (agentzh) 4.3.0.21-1
- upgraded openresty-stap to 4.3.0.21.
* Thu May 7 2020 Yichun Zhang (agentzh) 4.3.0.20-1
- upgraded openresty-stap to 4.3.0.20.
* Thu May 7 2020 Yichun Zhang (agentzh) 4.3.0.19-1
- upgraded openresty-stap to 4.3.0.19.
* Thu May 7 2020 Yichun Zhang (agentzh) 4.3.0.18-1
- upgraded openresty-stap to 4.3.0.18.
* Thu May 7 2020 Yichun Zhang (agentzh) 4.3.0.17-1
- upgraded openresty-stap to 4.3.0.17.
* Wed May 6 2020 Yichun Zhang (agentzh) 4.3.0.16-1
- upgraded openresty-stap to 4.3.0.16.
* Sun Apr 19 2020 Yichun Zhang (agentzh) 4.3.0.15-1
- upgraded openresty-stap to 4.3.0.15.
* Sat Apr 18 2020 Yichun Zhang (agentzh) 4.3.0.14-1
- upgraded openresty-stap to 4.3.0.14.
* Fri Apr 17 2020 Yichun Zhang (agentzh) 4.3.0.13-1
- upgraded openresty-stap to 4.3.0.13.
* Thu Apr 16 2020 Yichun Zhang (agentzh) 4.3.0.12-1
- upgraded openresty-stap to 4.3.0.12.
* Tue Apr 14 2020 Yichun Zhang (agentzh) 4.3.0.11-1
- upgraded openresty-stap to 4.3.0.11.
* Fri Mar 6 2020 Yichun Zhang (agentzh) 4.3.0.10-1
- upgraded openresty-stap to 4.3.0.10.
* Tue Mar 3 2020 Yichun Zhang (agentzh) 4.3.0.9-1
- upgraded openresty-stap to 4.3.0.9.
* Mon Feb 24 2020 Yichun Zhang (agentzh) 4.3.0.7-1
- upgraded openresty-stap to 4.3.0.7.
* Wed Jan 29 2020 Yichun Zhang (agentzh) 4.3.0.6-1
- upgraded openresty-stap to 4.3.0.6.
* Fri Jan 3 2020 Yichun Zhang (agentzh) 4.3.0.5-1
- upgraded openresty-stap to 4.3.0.5.
* Fri Jan 3 2020 Yichun Zhang (agentzh) 4.3.0.4-1
- upgraded openresty-stap to 4.3.0.4.
* Mon Dec 30 2019 Yichun Zhang (agentzh) 4.3.0.3-1
- upgraded openresty-stap to 4.3.0.3.
* Sat Dec 28 2019 Yichun Zhang (agentzh) 4.3.0.2-1
- upgraded openresty-stap to 4.3.0.2.
* Fri Dec 20 2019 Yichun Zhang (agentzh) 4.3.0.1-1
- upgraded openresty-stap to 4.3.0.1.
* Sun Dec 8 2019 Yichun Zhang (agentzh) 4.2.0.15-1
- upgraded openresty-stap to 4.2.0.15.
* Sun Nov 10 2019 Yichun Zhang (agentzh) 4.2.0.13-1
- upgraded openresty-stap to 4.2.0.13.
* Sun Nov 3 2019 Yichun Zhang (agentzh) 4.2.0.12-1
- upgraded openresty-stap to 4.2.0.12.
* Sun Oct 27 2019 Yichun Zhang (agentzh) 4.2.0.11-1
- upgraded openresty-stap to 4.2.0.11.
* Sun Oct 27 2019 Yichun Zhang (agentzh) 4.2.0.10-1
- upgraded openresty-stap to 4.2.0.10.
* Mon Oct 21 2019 Yichun Zhang (agentzh) 4.2.0.9-1
- upgraded openresty-stap to 4.2.0.9.
* Mon Sep 16 2019 Yichun Zhang (agentzh) 4.2.0.8-1
- upgraded openresty-stap to 4.2.0.8.
* Fri Sep 13 2019 Yichun Zhang (agentzh) 4.2.0.7-1
- upgraded openresty-stap to 4.2.0.7.
* Thu Aug 1 2019 Yichun Zhang (agentzh) 4.2.0.6-1
- upgraded openresty-stap to 4.2.0.6.
* Thu Aug 1 2019 Yichun Zhang (agentzh) 4.2.0.5-1
- upgraded openresty-stap to 4.2.0.5.
* Mon Jul 29 2019 Yichun Zhang (agentzh) 4.2.0.4-1
- upgraded openresty-stap to 4.2.0.4.
* Mon Jul 29 2019 Yichun Zhang (agentzh) 4.2.0.3-1
- upgraded openresty-stap to 4.2.0.3.
* Wed Jun 19 2019 Yichun Zhang (agentzh) 4.2.0.2-1
- upgraded openresty-stap to 4.2.0.2.
* Wed Jun 19 2019 Yichun Zhang (agentzh) 4.2.0.1-1
- upgraded openresty-stap to 4.2.0.1.
* Tue Sep 18 2018 Yichun Zhang 3.3.0.3
- upgraded to 3.3.0.3.
* Mon Aug 27 2018 Ming Wen 3.3.0.2
- initial build for openresty-stap.
