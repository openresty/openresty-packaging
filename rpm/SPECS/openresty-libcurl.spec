Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: openresty-libcurl
Version: 7.81.0.1
Release: 1%{?dist}
License: Proprietary
URL: https://curl.se/
Source0: curl-plus-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires: automake
BuildRequires: coreutils
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: make
BuildRequires: openresty-openssl111-devel
BuildRequires: openresty-zlib-devel
BuildRequires: perl-interpreter
BuildRequires: pkgconfig
BuildRequires: sed

%define curlprefix     /usr/local/openresty/libcurl
%define OPENSSL_PREFIX /usr/local/openresty/openssl111
%define OPENSSL_LIB    %{OPENSSL_PREFIX}/lib
%define OPENSSL_INC    %{OPENSSL_PREFIX}/include

%package devel
Summary: Libraries, includes, etc to develop with libcurl
Requires: %{name} = %{version}-%{release}

AutoReqProv:        no

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks.

%description devel
Development package for libcurl.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/curl-plus-%{version}"; \
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
%setup -q -n "curl-plus-%{version}"

# regenerate the configure script and Makefile.in files
autoreconf -fiv

%build
./configure \
    --prefix=%{curlprefix} \
    --disable-static     \
    --disable-ldap       \
    --disable-rtsp       \
    --disable-pthreads   \
    --disable-threaded-resolver \
    --disable-socketpair \
    --disable-ntlm       \
    --without-libpsl     \
    --without-nghttp2    \
    --without-ngtcp2     \
    --without-nghttp3    \
    --without-libidn2    \
    --without-quiche     \
    --without-brotli     \
    --without-zstd       \
    --with-openssl=$OPENSSL_PREFIX \
    LDFLAGS="-L$OPENSSL_PREFIX/lib -lssl -lcrypto \
    -Wl,-rpath,$OPENSSL_PREFIX/lib" CFLAGS="-O2 -g"

make -j`nproc`

%install
# install the executable and library that will be packaged as curl and libcurl
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# do not install /usr/share/fish/completions/curl.fish which is also installed
# by fish-3.0.2-1.module_f31+3716+57207597 and would trigger a conflict
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/fish
rm -fr ${RPM_BUILD_ROOT}%{curlprefix}/share
rm -f  ${RPM_BUILD_ROOT}/usr/share/doc

%files
%{curlprefix}/bin/curl
%{curlprefix}/bin/curl-config
%{curlprefix}/lib/libcurl.so
%{curlprefix}/lib/libcurl.so.4
%{curlprefix}/lib/libcurl.so.4.[0-9].[0-9]

%files devel
%defattr(-,root,root,-)
%dir %{curlprefix}/include
%{curlprefix}/include/curl/*.h
%{curlprefix}/lib/libcurl.la
%{curlprefix}/lib/pkgconfig/libcurl.pc

%changelog
* Thu Oct 3 2024 lijunlong <lijunlong@openrety.com> - 7.81.0.1
- first release
