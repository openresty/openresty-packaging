## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_TCPDUMP_VER := 4.9.3.2

.PHONY: openresty-tcpdump-download
openresty-tcpdump-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/tcpdump-plus-$(OPENRESTY_TCPDUMP_VER).tar.gz .
	rsync -av tcpdump-plus-$(OPENRESTY_TCPDUMP_VER).tar.gz openresty-tcpdump_$(OPENRESTY_TCPDUMP_VER).orig.tar.gz

openresty-tcpdump-clean:
	cd openresty-tcpdump && debclean
	-find openresty-tcpdump -maxdepth 1 ! -name 'debian' ! -name 'openresty-tcpdump' -print | xargs rm -rf
	rm -rf openresty-tcpdump*.deb
	rm -rf openresty-tcpdump_*.*

.PHONY: openresty-tcpdump-build
openresty-tcpdump-build: openresty-tcpdump-clean openresty-tcpdump-download
	sudo apt-get -y -q install automake openresty-pcap-dev ccache
	sudo apt-get -y -q --only-upgrade install  automake openresty-pcap-dev ccache
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-tcpdump_$(OPENRESTY_TCPDUMP_VER).orig.tar.gz --strip-components=1 -C openresty-tcpdump
	cd openresty-tcpdump \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
