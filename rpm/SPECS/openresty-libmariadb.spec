Name:               openresty-libmariadb
Version:            3.2.5.1
Release:            1%{?dist}
Summary:            The libmariadb library for OpenResty

Group:              System Environment/Libraries

License:            LGPL 2.1
URL:                https://github.com/orinc/mariadb-connector-c-plus
Source0:            mariadb-connector-c-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openresty-plus-openssl111-devel >= 1.1.1l-1

Requires:       openresty-plus-openssl111 >= 1.1.1l-1

AutoReqProv:        no

%define openssl_prefix       /usr/local/openresty-plus/openssl111
%define libmariadb_prefix    /usr/local/openresty-plus/libmariadb


%description
The mariadb client library for use by OpenResty ONLY

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/mariadb-connector-c-%{version}"; \
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

Summary:            Development files for OpenResty's mariadb client library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and library for OpenResty's mariadb library.


%prep
%setup -q -n mariadb-connector-c-%{version}


%build
cmake -DWITH_SSL=OPENSSL -DOPENSSL_ROOT_DIR=%{openssl_prefix} -DCMAKE_INSTALL_PREFIX=%{libmariadb_prefix} -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON -DWITH_UNIT_TESTS:BOOL=OFF .

make -j`nproc`


%install
make install PREFIX=%{libmariadb_prefix} DESTDIR=%{buildroot}
rm -fr  %{buildroot}/%{libmariadb_prefix}/man
rm -fr  %{buildroot}/%{libmariadb_prefix}/lib/pkgconfig
rm -fr  %{buildroot}/%{libmariadb_prefix}/lib/mariadb/libmariadbclient.a
rm -fr  %{buildroot}/%{libmariadb_prefix}/lib/mariadb/libmariadb.a


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%{libmariadb_prefix}/bin/mariadb_config
%{libmariadb_prefix}/lib/mariadb/libmariadb.so
%{libmariadb_prefix}/lib/mariadb/libmariadb.so.*
%{libmariadb_prefix}/lib/mariadb/plugin/*.so


%files devel
%defattr(-,root,root,-)

%{libmariadb_prefix}/include/mariadb/*.h
%{libmariadb_prefix}/include/mariadb/mysql/*.h
%{libmariadb_prefix}/include/mariadb/mariadb/*.h


%changelog
* Mon Feb 07 2022 Yichun Zhang 1.0.3.1
- initial version
