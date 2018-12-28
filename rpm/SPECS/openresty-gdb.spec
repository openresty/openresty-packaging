Name:           openresty-gdb
Version:        8.2.1
Release:        1%{?dist}
Summary:        gdb for OpenResty

License:        GPL
Group:          Development/Debuggers
URL:            https://www.gnu.org/home.en.html
Source0:        https://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.xz

AutoReqProv:    no


%define _prefix /usr/local/openresty-gdb
%define py_prefix /usr/local/openresty-python3

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires: glibc-devel
BuildRequires: make
BuildRequires: gcc gcc-c++
BuildRequires: texinfo
BuildRequires: mpfr-devel
BuildRequires: openresty-python3-devel >= 3.7.0-2
BuildRequires: xz-devel, ncurses-devel

Requires: openresty-python3 >= 3.7.0-2
Requires: xz-libs, gmp, mpfr, glibc, libstdc++, expat, ncurses-libs


%description
This is OpenResty's gdb package.


%prep
%setup -q -n gdb-%{version}


%build
CXXFLAGS="-g3 -O2 -I%{py_prefix}/include" \
    CFLAGS="-g3 -O2 -I%{py_prefix}/include" \
    LDFLAGS="-L%{py_prefix}/lib -Wl,-rpath,%{py_prefix}/lib" \
    ./configure --with-python=%{py_prefix}/bin/python3 \
    --prefix=%{_prefix} --without-guile

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
ln -sf /usr/lib/debug %{buildroot}/%{_prefix}/lib/


%files
%defattr(-,root,root)

%{_prefix}/bin/
%{_prefix}/lib/
%{_prefix}/share/
%exclude %{_prefix}/share/man/
%exclude %{_prefix}/share/info/
%exclude %{_prefix}/include/
%exclude %{_prefix}/lib/*.a
%exclude %{_prefix}/lib/*.la


%changelog
