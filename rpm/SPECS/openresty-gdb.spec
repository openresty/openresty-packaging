Name:           openresty-gdb
Version:        8.1
Release:        3%{?dist}
Summary:        gdb for OpenResty

License:        GPL
Group:          Development/Debuggers
URL:            https://www.gnu.org/home.en.html
Source0:        https://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.xz

AutoReqProv:    no


%define _prefix /usr/local/openresty-gdb

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires: glibc-devel
BuildRequires: make
BuildRequires: gcc gcc-c++
BuildRequires: texinfo
BuildRequires: mpfr-devel
BuildRequires: openresty-python3-devel >= 3.6.5-1

Requires: openresty-python3 >= 3.6.5-1


%description
This is OpenResty's gdb package


%prep
%setup -q -n gdb-%{version}


%build
PY_PREFIX=/usr/local/openresty-python3
GDB_PREFIX=%{_prefix}

LDFLAGS="-L$PY_PREFIX/lib -Wl,-rpath,$PY_PREFIX/lib" \
    ./configure --with-python=$PY_PREFIX/bin/python3 \
    --prefix=$GDB_PREFIX --without-guile

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
