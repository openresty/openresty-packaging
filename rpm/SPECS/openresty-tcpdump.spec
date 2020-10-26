Summary: A network traffic monitoring tool
Name: openresty-tcpdump
Version: 4.9.3.1
Release: 1%{?dist}.1
License: BSD with advertising
URL: http://www.tcpdump.org
Group: Applications/Internet
#Requires(pre): shadow-utils /usr/bin/getent
Requires: openresty-pcap >= 1.9.1
BuildRequires: automake
BuildRequires: openresty-pcap >= 1.9.1

%define tcpdump_prefix     /usr/local/openresty-tcpdump
%define pcap_prefix        /usr/local/openresty-pcap

Source0: tcpdump-plus-%{version}.tar.gz

%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces.  Tcpdump can display all of
the packet headers, or just the ones that match particular criteria.

Install tcpdump if you need a program to monitor network traffic.

%prep
%setup -q -n tcpdump-plus-%{version}

%build

export CC="ccache gcc -fdiagnostics-color=always -I%{pcap_prefix}/include"
export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -fno-strict-aliasing -DHAVE_GETNAMEINFO -I%{pcap_prefix}/include"
export LDFLAGS="-L%{pcap_prefix}/lib -Wl,-rpath,%{pcap_prefix}/lib"

./configure --with-user=tcpdump --without-smi --prefix=%{tcpdump_prefix}
make %{?_smp_mflags}


%install
mkdir -p ${RPM_BUILD_ROOT}%{tcpdump_prefix}/sbin
install -m755 tcpdump ${RPM_BUILD_ROOT}%{tcpdump_prefix}/sbin


%pre
if [ "$1" -eq 1 ]; then
  getent group  tcpdump > /dev/null ||  /usr/sbin/groupadd -g 72 tcpdump > /dev/null
  getent passwd tcpdump > /dev/null ||  /usr/sbin/useradd -u 72 -g 72 -s /sbin/nologin -M -r \
        -d / tcpdump > /dev/null
fi

exit 0

%files
%defattr(-,root,root)
%{tcpdump_prefix}/sbin/tcpdump

%changelog
* Wed Jun 17 2020 zhuizhuhaomeng 4.9.3
- initial build for tcpdump 4.9.3

