Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: openresty-curl
Version: 7.63.0
Release: 1%{?dist}
License: Proprietary
Source0: https://curl.se/download/curl-%{version}.tar.gz
# The curl download page ( https://curl.se/download.html ) links
# to Daniel's address page https://daniel.haxx.se/address.html for the GPG Key,
# which points to the GPG key as of April 7th 2016 of https://daniel.haxx.se/mykey.asc
#Source2: mykey.asc


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: curl = %{version}-%{release}
URL: https://curl.se/

BuildRequires: automake
BuildRequires: brotli-devel
BuildRequires: coreutils
BuildRequires: gcc
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn2-devel
BuildRequires: libnghttp2-devel
BuildRequires: libpsl-devel
BuildRequires: libssh-devel
BuildRequires: libtool
BuildRequires: make
BuildRequires: openldap-devel
BuildRequires: openssh-clients
BuildRequires: openssh-server
BuildRequires: openssl-devel
BuildRequires: perl-interpreter
BuildRequires: pkgconfig
BuildRequires: python3-devel
BuildRequires: sed
BuildRequires: zlib-devel

# require at least the version of libpsl that we were built against,
# to ensure that we have the necessary symbols available (#1631804)
%global libpsl_version %(pkg-config --modversion libpsl 2>/dev/null || echo 0)

# require at least the version of libssh that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%global libssh_version %(pkg-config --modversion libssh 2>/dev/null || echo 0)

# require at least the version of openssl-libs that we were built against,
# to ensure that we have the necessary symbols available (#1462184, #1462211)
# (we need to translate 3.0.0-alpha16 -> 3.0.0-0.alpha16 and 3.0.0-beta1 -> 3.0.0-0.beta1 though)
%global openssl_version %({ pkg-config --modversion openssl 2>/dev/null || echo 0;} | sed 's|-|-0.|')

%define curlprefix            %{_usr}/local/%{name}

AutoReqProv:        no

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/curl-%{version}"; \
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
%setup -q -n "curl-%{version}"

# regenerate the configure script and Makefile.in files
autoreconf -fiv

%build
export common_configure_opts=" \
    --cache-file=../config.cache \
    --disable-static \
    --enable-symbol-hiding \
    --enable-ipv6 \
    --enable-threaded-resolver \
    --with-gssapi \
    --with-nghttp2 \
    --with-ssl --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt"

./configure $common_configure_opts \
        --prefix=/usr/local/openresty-curl/ \
        --enable-ldap \
        --enable-ldaps \
        --enable-manual \
        --with-brotli \
        --with-libidn2 \
        --with-libpsl \
        --with-libssh

make -j`nproc`

%install
# install the executable and library that will be packaged as curl and libcurl
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# do not install /usr/share/fish/completions/curl.fish which is also installed
# by fish-3.0.2-1.module_f31+3716+57207597 and would trigger a conflict
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/fish
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la
rm -fr ${RPM_BUILD_ROOT}%{curlprefix}/include
rm -fr ${RPM_BUILD_ROOT}%{curlprefix}/share
rm -f  ${RPM_BUILD_ROOT}%{curlprefix}/bin/curl-config
rm -f  ${RPM_BUILD_ROOT}%{curlprefix}/lib/libcurl.la
rm -f  ${RPM_BUILD_ROOT}%{curlprefix}/lib/libcurl.so
rm -f  ${RPM_BUILD_ROOT}%{curlprefix}/lib/pkgconfig/libcurl.pc
rm -f  ${RPM_BUILD_ROOT}/usr/share/aclocal/libcurl.m4

%files
%doc COPYING
%doc CHANGES
%doc README
%doc docs/FAQ
%doc docs/TODO
%{curlprefix}/bin/curl
%{curlprefix}/lib/libcurl.so.4
%{curlprefix}/lib/libcurl.so.4.[0-9].[0-9]

%changelog
* Tue Sep 28 2021 lijunlong <lijunlong@openrety.com> - 7.63.0-1
- first release
