Name:           openresty-python3
Version:        3.6.5
Release:        1%{?dist}
Summary:        python3 for OpenResty

Group:          Development/Languages
License:        PSFL
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz

AutoReqProv:    no


%define _prefix /usr/local/openresty-python3

%global __os_install_post     %{nil}


%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires: glibc-devel
BuildRequires: gcc-c++
BuildRequires: make


%description
This is OpenResty's python3 package


%package devel
Summary: Libraries and header files needed for Python development
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.


%prep
%setup -q -n Python-%{version}


%build
export PYTHONPATH=
PY_PREFIX=/usr/local/openresty-python3
./configure --prefix=$PY_PREFIX --enable-shared --enable-ipv6 \
    LDFLAGS="-L$PY_PREFIX/lib -Wl,-rpath,$PY_PREFIX/lib"
make %{?_smp_mflags}


%install
make \
    DESTDIR=%{buildroot} \
    INSTALL="install -p" \
    install


%files
%defattr(-, root, root)

%{_prefix}/bin/*
%{_prefix}/lib/*
%exclude %{_prefix}/share/*
%exclude %{_prefix}/lib/python3.6/config-3.6m-x86_64-linux-gnu


%files devel
%defattr(-, root, root)

%{_prefix}/include/*
%{_prefix}/lib/python3.6/config-3.6m-x86_64-linux-gnu


%changelog
