Summary:            Advanced IP routing and network device configuration tools
Name:               openresty-iproute2
Version:            4.13.0
Release:            2%{?dist}
Group:              Applications/System
URL:                http://kernel.org/pub/linux/utils/net/iproute2/
Source0:            http://kernel.org/pub/linux/utils/net/iproute2/iproute2-%{version}.tar.xz
AutoReqProv:        no

%define _prefix     /usr/local/openresty-iproute2
%define _sysconfdir %_prefix/etc

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

License:            GPLv2+ and Public Domain
BuildRequires:      openresty-kernel-cross-headers >= 4.9
BuildRequires:      bison
BuildRequires:      elfutils-libelf-devel
BuildRequires:      flex
BuildRequires:      iptables-devel >= 1.4.5
BuildRequires:      libdb-devel
BuildRequires:      libmnl-devel
BuildRequires:      libselinux-devel
BuildRequires:      pkgconfig

# For the UsrMove transition period
Conflicts:          filesystem < 3
Provides:           %_prefix/sbin/ip

%description
The iproute package contains networking utilities (ip and rtmon, for example)
which are designed to use the advanced networking capabilities of the Linux
kernel.

%prep
%setup -q -n iproute2-%{version}

%build
export CFLAGS="%{optflags} -I /usr/x86-linux-gnu/include/"
export LIBDIR=/%{_libdir}
export IPT_LIB_DIR=/%{_lib}/xtables
./configure
make %{?_smp_mflags}

%install
export DESTDIR='%{buildroot}'
export SBINDIR='%{_sbindir}'
export MANDIR='%{_mandir}'
export LIBDIR='%{_libdir}'
export CONFDIR='%{_sysconfdir}/iproute2'
export DOCDIR='%{_docdir}'
export PREFIX='%{_prefix}'
make install

# drop these files, iproute-doc package extracts files directly from _builddir
rm -rf '%{buildroot}%{_docdir}'

%files
%dir %{_sysconfdir}/iproute2
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%{_libdir}/*
%exclude %{_datadir}/*
%exclude %{_includedir}/*
