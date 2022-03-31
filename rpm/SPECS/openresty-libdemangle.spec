Name:               openresty-libdemangle
Version:            11.2.0
Release:            1%{?dist}
Summary:            The C++ demangle library for OpenResty Plus

Group:              System Environment/Libraries

License:            LGPL
URL:                https://gcc.gnu.org/mirrors.html
Source0:            https://github.com/gcc-mirror/gcc/archive/refs/tags/releases/gcc-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:

AutoReqProv:        no

%define libdemangle_prefix      /usr/local/openresty-libdemangle


%description
This is a library that provides an API for parsing C++ demangle names.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openresty-libdemangle-%{version}"; \
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

Summary:            Development files for OpenResty's libdemangle library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
This is a library that provides an API for parsing C++ demangle names.


%prep
# The $PWD is rpmbuild/BUILD
%setup -q -n "gcc-releases-gcc-%{version}"


%build
export JOBS=${JOBS:-9}
cd ./libiberty/
CFLAGS=-fPIC ./configure
make -j${JOBS} > /dev/stderr
cc -shared ./cp-demangle.o ./rust-demangle.o ./d-demangle.o ./cplus-dem.o ./cp-demint.o ./safe-ctype.o -o libdemangle.so


%install
mkdir -p $RPM_BUILD_ROOT/%{libdemangle_prefix}/lib
mkdir -p $RPM_BUILD_ROOT/%{libdemangle_prefix}/include

install -m 755 ./libiberty/libdemangle.so $RPM_BUILD_ROOT/%{libdemangle_prefix}/lib/
install -m 644 ./include/demangle.h $RPM_BUILD_ROOT/%{libdemangle_prefix}/include/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{libdemangle_prefix}/lib/libdemangle.so*


%files devel
%defattr(-,root,root,-)

%{libdemangle_prefix}/include/demangle.h


%changelog
* Mon Mar 23 2022 Yichun Zhang 11.2.0
- initial version
