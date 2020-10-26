Name: openresty-pcap
Version: 1.9.1
Release: 1%{?dist}
Summary: A system-independent interface for user-level packet capture
Group: Development/Libraries
License: BSD with advertising
URL: http://www.tcpdump.org
BuildRequires: glibc-kernheaders >= 2.2.0
BuildRequires: bison
BuildRequires: flex

%define  pcap_prefix /usr/local/openresty-pcap

Source0: https://www.tcpdump.org/release/libpcap-%{version}.tar.gz

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

%package devel
Summary: Libraries and header files for the libpcap library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

This package provides the libraries, include files, and other
resources needed for developing libpcap applications.

%prep
%setup -q -n libpcap-libpcap-%{version}

#sparc needs -fPIC
%ifarch %{sparc}
sed -i -e 's|-fpic|-fPIC|g' configure
%endif

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
./configure --prefix=%{pcap_prefix} --libdir=%{pcap_prefix}/lib
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf %{buildroot}/%{pcap_prefix}/bin
rm -rf %{buildroot}/%{pcap_prefix}/share
rm -rf %{buildroot}/%{pcap_prefix}/lib/pkgconfig

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pcap_prefix}/lib/libpcap.so*
%{pcap_prefix}/lib/libpcap.a

%files devel
%defattr(-,root,root)
%{pcap_prefix}/include/

%changelog
* Wed Jun 17 2020 zhuizhuhaomeng 1.9.1
- initial build for pcap 1.9.1
