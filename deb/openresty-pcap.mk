## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PCAP_VER := 1.9.1

.PHONY: openresty-pcap-download
openresty-pcap-download:
	wget -nH --cut-dirs=100 --mirror 'https://www.tcpdump.org/release/libpcap-$(OPENRESTY_PCAP_VER).tar.gz'
	rm -rf openresty-pcap_$(OPENRESTY_PCAP_VER)
	mkdir -p openresty-pcap_$(OPENRESTY_PCAP_VER)
	tar -xf libpcap-$(OPENRESTY_PCAP_VER).tar.gz --strip-components=1 -C openresty-pcap_$(OPENRESTY_PCAP_VER)
	tar -czf openresty-pcap_$(OPENRESTY_PCAP_VER).orig.tar.gz openresty-pcap_$(OPENRESTY_PCAP_VER)

openresty-pcap-clean:
	cd openresty-pcap && debclean
	-find openresty-pcap -maxdepth 1 ! -name 'debian' ! -name 'openresty-pcap' -print | xargs rm -rf
	rm -rf openresty-pcap*.deb
	rm -rf openresty-pcap_*.*

.PHONY: openresty-pcap-build
openresty-pcap-build: openresty-pcap-clean openresty-pcap-download
	sudo apt-get -y -q install bison flex
	sudo apt-get -y -q --only-upgrade install bison flex
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-pcap_$(OPENRESTY_PCAP_VER).orig.tar.gz --strip-components=1 -C openresty-pcap
	cd openresty-pcap \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
