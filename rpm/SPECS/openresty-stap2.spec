Name:           openresty-stap2
Version:        4.9.0.23
Release:        1%{?dist}
Summary:        OpenResty's fork of SystemTap
Group:          Development/System
License:        GPLv2+
URL:            http://sourceware.org/systemtap/
Provides:       openresty-stap2

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
Requires: openresty-stap2-runtime = %{version}-%{release}
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
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/systemtap-plus2-%{version}"; \
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
%setup -q -n systemtap-plus2-%{version}


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
* Wed Feb 28 2024 Jiahao Wang 4.9.0.23
- initial build for openresty-stap2.
