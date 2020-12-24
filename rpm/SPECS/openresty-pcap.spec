Name: openresty-pcap
Version: 1.9.1
Release: 3%{?dist}
Summary: A system-independent interface for user-level packet capture
Group: Development/Libraries
License: BSD with advertising
URL: http://www.tcpdump.org

%if 0%{?suse_version}
BuildRequires: linux-glibc-devel
%else
BuildRequires: kernel-headers
%endif

BuildRequires: bison, flex, ccache
AutoReqProv: no

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


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/libpcap-%{version}"; \
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
%setup -q -n libpcap-%{version}


%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -g3"
./configure --prefix=%{pcap_prefix} --libdir=%{pcap_prefix}/lib
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf %{buildroot}/%{pcap_prefix}/bin
rm -rf %{buildroot}/%{pcap_prefix}/share
rm -rf %{buildroot}/%{pcap_prefix}/lib/pkgconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{pcap_prefix}/lib/libpcap.so.*

%files devel
%defattr(-,root,root)
%{pcap_prefix}/include/
%{pcap_prefix}/lib/libpcap.a
%{pcap_prefix}/lib/libpcap.so

%changelog
* Wed Jun 17 2020 zhuizhuhaomeng 1.9.1
- initial build for pcap 1.9.1
