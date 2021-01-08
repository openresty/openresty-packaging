Name:       openresty-nodejs
Version:    15.4.0
Release:    1
Summary:    OpenResty's fork of JavaScript runtime
License:    MIT and ASL 2.0 and ISC and BSD
Group:      Development/Languages
URL:        http://nodejs.org/

Source0:    https://nodejs.org/dist/v%{version}/node-v%{version}.tar.xz

BuildRequires: openresty-python3 >= 3.7.9-13
BuildRequires: ccache, gcc, gcc-c++
BuildRequires: openresty-saas-zlib-devel
BuildRequires: openresty-saas-openssl111-devel >= 1.1.1i
Requires: openresty-saas-zlib
Requires: openresty-saas-openssl111 >= 1.1.1i

AutoReqProv: no

%define     _prefix /usr/local/openresty-nodejs
%define     zlib_prefix     /opt/openresty-saas/zlib
%define     openssl_prefix  /opt/openresty-saas/openssl111
%define     py3_prefix  /usr/local/openresty-python3


%description
Node.js is a platform built on Chrome's JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.
This Node.js build is specifically for OpenResty uses.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/node-v%{version}"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%endif

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages

%global __brp_mangle_shebangs_exclude_from *
%endif

%if 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%prep
%setup -q -n node-v%{version}


%package devel
Summary: JavaScript runtime - development headers
Group: Development/Languages
Requires: %{name} = %{version}-%{release}%{?dist}

%description devel
Development headers for the OpenResty's fork of Node.js.


%package npm
Summary: OpenResty's fork of Node.js Package Manager
Requires: openresty-nodejs = %{version}-%{release}


%description npm
npm is a package manager for node.js. You can use it to install and publish
your node programs. It manages dependencies and does other cool stuff.
This npm build is specifically for OpenResty uses.


%build
export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0
export LDFLAGS="%{?__global_ldflags} -Wl,-rpath,%{openssl_prefix}/lib:%{zlib_prefix}/lib:%{_prefix}/lib"
export CC="ccache gcc"
export CXX="ccache g++"
export CFLAGS='-g -O2 -D_FILE_OFFSET_BITS=64 -DZLIB_CONST -fno-delete-null-pointer-checks -D_LARGEFILE_SOURCE'
export CXXFLAGS="$CFLAGS"
export PATH="%{py3_prefix}/bin:$PATH"

${py3_prefix}/bin/python3 ./configure --prefix=%{_prefix} --without-dtrace \
    --shared \
    --with-intl=small-icu --gdb \
    --shared-zlib --shared-zlib-includes=%{zlib_prefix}/include \
    --shared-zlib-libpath=%{zlib_prefix}/lib \
    --shared-openssl --shared-openssl-includes=%{openssl_prefix}/include \
    --shared-openssl-libpath=%{openssl_prefix}/lib

make V=0 BUILDTYPE=Release \
    LD_LIBRARY_PATH="%{openssl_prefix}/lib:$LD_LIBRARY_PATH" \
    %{?_smp_mflags}

%install
export PATH="$PATH:/usr/local/openresty-python3/bin"

rm -rf %{buildroot}
${py3_prefix}/bin/python3 tools/install.py install '%{buildroot}' '%{_prefix}'
install -m 0755 out/Release/node %{buildroot}%{_prefix}/bin/
(cd %{buildroot}%{_prefix}/lib; ln -sf libnode.so.88 libnode.so)

rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/lib/node_modules/npm/{docs,man,changelogs}
rm -f %{buildroot}%{_prefix}/lib/node_modules/npm/{AUTHORS,CHANGELOG.md,CONTRIBUTING.md,LICENSE,make.bat,Makefile,README.md}

sed -i 's/^\#\!\/usr\/bin\/env python$/\#\!\/usr\/bin\/env python3/' `find %{buildroot}/ -name '*.py'`
sed -i 's/^\#\!\/usr\/bin\/python$/\#\!\/usr\/bin\/python3/' `find %{buildroot}/ -name '*.py'`


%files
%attr(0755,root,root) %{_prefix}/bin/node
%{_prefix}/lib/libnode.so
%{_prefix}/lib/libnode.so.88


%files devel
%{_prefix}/include/node


%files npm
%{_prefix}/bin/npm
%{_prefix}/bin/npx
%{_prefix}/lib/node_modules/npm


%clean
rm -rf %{buildroot}


%changelog
* Mon Jan 4 2021 Jiahao Wang (jiahao) 15.4.0-1.
- initial build for openresty-nodejs 15.4.0.
