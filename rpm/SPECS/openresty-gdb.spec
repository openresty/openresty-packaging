Name:           openresty-gdb
Version:        9.2
Release:        4%{?dist}
Summary:        gdb for OpenResty

License:        GPL
Group:          Development/Debuggers
URL:            https://www.gnu.org/home.en.html
Source0:        https://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.xz

AutoReqProv:    no


%define _prefix /usr/local/openresty-gdb
%define py_prefix /usr/local/openresty-python3


BuildRequires: glibc-devel
BuildRequires: make
BuildRequires: ccache, gcc, gcc-c++
BuildRequires: texinfo
BuildRequires: mpfr-devel
BuildRequires: openresty-python3-devel >= 3.7.9
BuildRequires: xz-devel, ncurses-devel

Requires: openresty-python3 >= 3.7.9

%if 0%{?suse_version}
Requires: liblzma5
Requires: libstdc++6

%if %{suse_version} <= 1315
Requires: libmpfr4
%else
Requires: libmpfr6
%endif

Requires: libgmp10
Requires: libncurses6
%else
Requires: libstdc++
Requires: mpfr
Requires: xz-libs
Requires: gmp
Requires: ncurses-libs
%endif

Requires: expat


%description
This is OpenResty's gdb package.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/gdb-%{version}"; \
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
%setup -q -n gdb-%{version}


%build

mkdir -p build
cd build/

CXXFLAGS="-g3 -O2 -I%{py_prefix}/include" \
    CFLAGS="-g3 -O2 -I%{py_prefix}/include" \
    LDFLAGS="-L. -L%{py_prefix}/lib -Wl,-rpath,%{py_prefix}/lib" \
    CC='ccache gcc -fdiagnostics-color=always' \
    CXX='ccache g++ -fdiagnostics-color=always' \
    ../configure --with-python="%{py_prefix}/bin/python3" \
    --libdir="%{_prefix}/lib" \
    --prefix=%{_prefix} --without-guile

make %{?_smp_mflags} > /dev/null


%install

cd build/
make install DESTDIR=%{buildroot} > /dev/null
ln -sf /usr/lib/debug %{buildroot}/%{_prefix}/lib/

rm -rf %{buildroot}%{_prefix}/include/
rm -rf %{buildroot}%{_prefix}/lib/*.a
rm -rf %{buildroot}%{_prefix}/lib/*.la
rm -rf %{buildroot}%{_prefix}/share/man/
rm -rf %{buildroot}%{_prefix}/share/info/

export QA_RPATHS=$[ 0x0002 ]


%files
%defattr(-,root,root)

%{_prefix}/bin/
%{_prefix}/lib/
%{_prefix}/share/


%changelog
