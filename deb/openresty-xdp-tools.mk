## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_XDP_TOOLS_VER := 1.2.2

.PHONY: openresty-xdp-tools-download
openresty-xdp-tools-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/xdp-tools-plus-$(OPENRESTY_XDP_TOOLS_VER).tar.gz ./
	rm -rf openresty-xdp-tools_$(OPENRESTY_XDP_TOOLS_VER)
	mkdir -p openresty-xdp-tools_$(OPENRESTY_XDP_TOOLS_VER)
	tar -xf xdp-tools-plus-$(OPENRESTY_XDP_TOOLS_VER).tar.gz --strip-components=1 -C openresty-xdp-tools_$(OPENRESTY_XDP_TOOLS_VER)
	tar -czf openresty-xdp-tools_$(OPENRESTY_XDP_TOOLS_VER).orig.tar.gz openresty-xdp-tools_$(OPENRESTY_XDP_TOOLS_VER)

openresty-xdp-tools-clean:
	-cd openresty-xdp-tools && debclean
	-find openresty-xdp-tools -maxdepth 1 ! -name 'debian' ! -name 'openresty-xdp-tools' -print | xargs rm -rf
	rm -rf openresty-xdp-tools*.deb
	rm -rf openresty-xdp-tools_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-xdp-tools-build
openresty-xdp-tools-build: openresty-xdp-tools-clean openresty-xdp-tools-download
	sudo apt-get -y -q install ccache gcc make perl pkg-config openresty-libbpf-net-dev openresty-pcap-dev openresty-elfutils-dev openresty-llvm zlib1g-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl pkg-config openresty-libbpf-net-dev openresty-pcap-dev openresty-elfutils-dev openresty-llvm zlib1g-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-xdp-tools_$(OPENRESTY_XDP_TOOLS_VER).orig.tar.gz --strip-components=1 -C openresty-xdp-tools
	cd openresty-xdp-tools \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define distro=$(DISTRO) debian/control.tt2 > debian/control \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
