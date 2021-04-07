Summary: A network traffic monitoring tool
Name: openresty-tcpdump
Version: 4.9.3.3
Release: 2%{?dist}
License: BSD with advertising
URL: http://www.tcpdump.org
Group: Applications/Internet
#Requires(pre): shadow-utils /usr/bin/getent
Requires: openresty-pcap >= 1.9.1
BuildRequires: automake, openresty-pcap-devel >= 1.9.1, ccache
AutoReqProv: no

%define tcpdump_prefix     /usr/local/openresty-tcpdump
%define pcap_prefix        /usr/local/openresty-pcap

Source0: tcpdump-plus-%{version}.tar.gz


%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces.  Tcpdump can display all of
the packet headers, or just the ones that match particular criteria.

Install tcpdump-plus if you need a program to monitor network traffic.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tcpdump-plus-%{version}"; \
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
%setup -q -n tcpdump-plus-%{version}


%build

export CC="ccache gcc -fdiagnostics-color=always -I%{pcap_prefix}/include"
export CFLAGS="-g3 $RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -fno-strict-aliasing -DHAVE_GETNAMEINFO -I%{pcap_prefix}/include"
export LDFLAGS="-L%{pcap_prefix}/lib -Wl,-rpath,%{pcap_prefix}/lib"

./configure --with-user=tcpdump --without-smi --prefix=%{tcpdump_prefix} --with-system-libpcap \
--without-crypto
make -j`nproc`

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{tcpdump_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{tcpdump_prefix}/bin
install -m755 tcpdump-plus ${RPM_BUILD_ROOT}%{tcpdump_prefix}/sbin
install -m755 hex2pcap ${RPM_BUILD_ROOT}%{tcpdump_prefix}/bin

export QA_RPATHS=$[ 0x0002 ]


%pre
if [ "$1" -eq 1 ]; then
  getent group  tcpdump > /dev/null ||  /usr/sbin/groupadd -g 72 tcpdump > /dev/null
  getent passwd tcpdump > /dev/null ||  /usr/sbin/useradd -u 72 -g 72 -s /sbin/nologin -M -r \
        -d / tcpdump > /dev/null
fi

exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{tcpdump_prefix}/sbin/tcpdump-plus
%{tcpdump_prefix}/bin/hex2pcap

%changelog
* Fri Oct 30 2020 Yichun Zhang (agentzh) 4.9.3.3-1
- upgraded tcpdump-plus to 4.9.3.3.
* Wed Oct 28 2020 Yichun Zhang (agentzh) 4.9.3.2-1
- upgraded tcpdump-plus to 4.9.3.2.
* Wed Jun 17 2020 zhuizhuhaomeng 4.9.3
- initial build for tcpdump 4.9.3

