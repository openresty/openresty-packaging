Name:               openresty-libmemcached
Version:            1.2.2
Release:            3%{?dist}
Summary:            The libmemcached library for OpenResty

Group:              System Environment/Libraries

License:            BSD
URL:                https://github.com/simplegeo/libmemcached
Source0:            libmemcached-plus-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool, autoconf, automake, bison, flex, openresty-cyrus-sasl-devel
BuildRequires:  openresty-plus-openssl111-devel >= 1.1.1l-1

Requires:       openresty-plus-openssl111 >= 1.1.1l-1, openresty-cyrus-sasl

AutoReqProv:        no

%define openssl_prefix     /usr/local/openresty-plus/openssl111
%define sasl_prefix        /usr/local/openresty-plus/cyrus-sasl
%define libmemcached_prefix     /usr/local/openresty-plus/libmemcached


%description
The libmemcached library for OpenResty ONLY

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/libmemcached-plus-%{version}"; \
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


%package devel

Summary:            Development files for OpenResty's libmemcached library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and library for OpenResty's libmemcached library.


%prep
%setup -q -n libmemcached-plus-%{version}


%build
autoreconf -ivf
CXXFLAGS="-I%{sasl_prefix}/include -Wno-error=unsafe-loop-optimizations" \
    LDFLAGS="-L%{sasl_prefix}/lib -Wl,-rpath,%{sasl_prefix}/lib" \
    ./configure --prefix=%{libmemcached_prefix} \
    --libdir=%{libmemcached_prefix}/lib \
    --with-memcached=false \
    --enable-libmemcachedprotocol --enable-shared --disable-docs \
    --disable-static --with-memcached=false

make -j`nproc`


%install
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}/%{libmemcached_prefix}/bin
rm -fr %{buildroot}/%{libmemcached_prefix}/share
rm -rf %{buildroot}/%{libmemcached_prefix}/lib/*.la
rm -rf %{buildroot}/%{libmemcached_prefix}/lib/pkgconfig

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%{libmemcached_prefix}/lib/libhashkit.so
%{libmemcached_prefix}/lib/libhashkit.so.2
%{libmemcached_prefix}/lib/libhashkit.so.2.0.0
%{libmemcached_prefix}/lib/libmemcached.so
%{libmemcached_prefix}/lib/libmemcached.so.11
%{libmemcached_prefix}/lib/libmemcached.so.11.0.0
%{libmemcached_prefix}/lib/libmemcachedutil.so
%{libmemcached_prefix}/lib/libmemcachedutil.so.2
%{libmemcached_prefix}/lib/libmemcachedutil.so.2.0.0


%files devel
%defattr(-,root,root,-)

%{libmemcached_prefix}/include/libhashkit/*.h
%{libmemcached_prefix}/include/libhashkit-1.0/*.h
%{libmemcached_prefix}/include/libhashkit-1.0/*.hpp
%{libmemcached_prefix}/include/libmemcached-1.2/*.h
%{libmemcached_prefix}/include/libmemcached-1.2/*.hpp
%{libmemcached_prefix}/include/libmemcached-1.2/memcached/*.h
%{libmemcached_prefix}/include/libmemcached-1.2/struct/*.h
%{libmemcached_prefix}/include/libmemcached-1.2/types/*.h
%{libmemcached_prefix}/include/libmemcachedutil-1.2/*.h
%{libmemcached_prefix}/include/libmemcachedutil-1.2/*.hpp



%changelog
* Fri Mar 11 2022 Yichun Zhang (agentzh) 1.2.2-1
- upgraded libmemcached to 1.2.2.
* Mon Feb 07 2022 Yichun Zhang 1.0.3.1
- initial version
