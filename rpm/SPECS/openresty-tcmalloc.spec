%define     pkgname     gperftools
%define     orprefix    /usr/local/openresty-tcmalloc

Name:		openresty-tcmalloc
Version:	2.9.1
Release:	3%{?dist}
License:	BSD
Summary:	Very fast malloc and performance analysis tools
Group:      System Environment/Libraries
URL:		https://github.com/gperftools/gperftools
Source0:	https://github.com/gperftools/gperftools/archive/%{pkgname}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:	autoconf, automake, libtool

%description
Perf Tools is a collection of performance analysis tools, including a
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly heap-checker,
a heap profiler, and a cpu-profiler.

This is a metapackage which pulls in all of the gperftools (and pprof)
binaries, libraries, and development headers, so that you can use them.

This Perf Tools build is specifically for OpenResty uses.

%package devel
Summary:            Development files for %{name}
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}

%description devel
Libraries and headers for developing applications that use gperftools.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{pkgname}-%{version}"; \
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
%setup -qn %{pkgname}-%{version}

# No need to have exec permissions on source code
chmod -x src/*.h src/*.cc

autoreconf -ifv

%build
CFLAGS=`echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-unused-local-typedefs -DTCMALLOC_LARGE_PAGES | sed -e 's|-fexceptions||g'`
CXXFLAGS=`echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-unused-local-typedefs -DTCMALLOC_LARGE_PAGES | sed -e 's|-fexceptions||g'`
./configure \
    --prefix=%{orprefix} \
    --libdir=%{orprefix}/lib \
	--disable-dynamic-sized-delete-support \
	--disable-static

# Bad rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Can't build with smp_mflags
make -j`nproc`

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -rf %{buildroot}%{orprefix}/share
# remove pprof
rm -f %{buildroot}%{orprefix}/bin/pprof
rm -f %{buildroot}%{orprefix}/bin/pprof-symbolize

%files
%{orprefix}/lib/*.so
%{orprefix}/lib/*.so.*

%files devel
%{orprefix}/include/google/
%{orprefix}/include/gperftools/
%{orprefix}/lib/pkgconfig/*.pc

%changelog
* Mon Feb 28 2022 Jiahao Wang <wangjiahao@openresty.com> - 2.9.1-1
- Upgraded to 2.9.1.
