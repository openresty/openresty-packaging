Name:           openresty-python3
Version:        3.7.0
Release:        2%{?dist}
Summary:        python3 for OpenResty

Group:          Development/Languages
License:        PSFL
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz

AutoReqProv:    no


%define _prefix /usr/local/openresty-python3

%global __os_install_post     %{nil}


%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRequires: glibc-devel
BuildRequires: gcc
BuildRequires: make
BuildRequires: libffi-devel

Requires: libffi


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
./configure --prefix=%{_prefix} --enable-shared --enable-ipv6 \
    LDFLAGS="-L%{_prefix}/lib -Wl,-rpath,%{_prefix}/lib"
make %{?_smp_mflags}


%install
make \
    DESTDIR=%{buildroot} \
    INSTALL="install -p" \
    install

find %{buildroot} -type f -print0 | xargs -0 chmod u+w

%files
%defattr(-, root, root)

%{_prefix}/bin/*
%{_prefix}/lib/*
%exclude %{_prefix}/share/*
%exclude %{_prefix}/lib/python*/config-*-x86_64-linux-gnu


%files devel
%defattr(-, root, root)

%{_prefix}/include/*
%{_prefix}/lib/python*/config-*-x86_64-linux-gnu


%changelog
