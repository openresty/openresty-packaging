Name:           openresty-keepalived
Version:        2.2.1
Release:        1%{?dist}
Summary:        OpenResty Fork's of keepalived.

Group:          Development/System

License:        GPLv2
URL:            https://www.keepalived.org/
Source0:        https://www.keepalived.org/software/keepalived-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake, autoconf
BuildRequires:  ccache, gcc
BuildRequires:  make
BuildRequires:  openresty-plus-openssl111-devel >= 1.1.1i
BuildRequires:  libnl3-devel
Requires: libnl3
Requires: openresty-plus-openssl111 >= 1.1.1i

AutoReqProv: no
AutoReq:     no
AutoProv:    no

%define prefix      /usr/local/openresty-keepalived
%define ssl_prefix  /usr/local/openresty-plus/openssl111

%description
The main goal of this project is to provide simple and robust facilities for
loadbalancing and high-availability to Linux system and Linux based infrastructures.

This is OpenResty's keepalived package.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/keepalived-%{version}"; \
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
# The $PWD is rpmbuild/BUILD
%setup -q -n "keepalived-%{version}"

%build
./build_setup
CC='ccache gcc -fdiagnostics-color=always' \
CFLAGS="-I%{ssl_prefix}/include" \
LDFLAGS='-L%{ssl_prefix}/lib -Wl,-rpath,%{ssl_prefix}/lib' \
    ./configure --prefix=%{prefix} \
    --disable-systemd \
    --enable-sha1 --enable-strict-config-checks \
    --enable-log-file

make -j`nproc`

%install
make install-exec DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}


%files
%{prefix}/bin/genhash
%{prefix}/sbin/keepalived

%changelog
* Thu Feb 25 2021 Jiahao Wang 2.2.1-1
- initial build for openresty-keepalived
