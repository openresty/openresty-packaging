Name:               openresty-cyrus-sasl
Version:            2.1.28
Release:            1%{?dist}
Summary:            This is the Cyrus SASL API implementation. It can be used on the client or server side to provide authentication and authorization services. 

Group:              System Environment/Libraries

License:            https://github.com/cyrusimap/cyrus-sasl/blob/master/COPYING
URL:                https://github.com/cyrusimap/cyrus-sasl
Source0:     https://github.com/cyrusimap/cyrus-sasl/releases/download/cyrus-sasl-%{version}/cyrus-sasl-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      libtool

AutoReqProv:        no

%define sasl_prefix     /usr/local/openresty/cyrus-sasl


%description
This is the Cyrus SASL API implementation. It can be used on the client or server side to provide authentication and authorization services.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/cyrus-sasl-%{version}"; \
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

Summary:            Development files for OpenResty's cyrus-sasl library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty's cyrus-sasl library.


%prep
%setup -q -n cyrus-sasl-%{version}


%build
./configure --prefix=%{sasl_prefix} --enable-gssapi=no --with-openssl=/usr/local/openresty/openssl111
make -j`nproc` > /dev/stderr


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{sasl_prefix}/share
rm -rf  %{buildroot}/%{sasl_prefix}/sbin
rm -f  %{buildroot}/%{sasl_prefix}/lib/*.la
rm -f  %{buildroot}/%{sasl_prefix}/lib/sasl2/*.la


%clean
rm -rf %{buildroot}


%files
%{sasl_prefix}/lib/*.so
%{sasl_prefix}/lib/*.so.*
%{sasl_prefix}/lib/sasl2/*.so
%{sasl_prefix}/lib/sasl2/*.so.*


%files devel
%{sasl_prefix}/include/sasl/*.h
%{sasl_prefix}/lib/pkgconfig/*.pc


%changelog
* Fri Mar 4 2022 Yichun Zhang (agentzh) 2.1.28-1
- upgraded openresty-cyrus-sasl to 2.1.28.
