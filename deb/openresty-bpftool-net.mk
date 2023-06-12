## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_BPFTOOL_NET_VER := 5.13.18.7

.PHONY: openresty-bpftool-net-download
openresty-bpftool-net-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/bpftool-plus-$(OPENRESTY_BPFTOOL_NET_VER).tar.gz ./
	rm -rf openresty-bpftool-net_$(OPENRESTY_BPFTOOL_NET_VER)
	mkdir -p openresty-bpftool-ne_$(OPENRESTY_BPFTOOL_NET_VER)
	tar -xf bpftool-plus-$(OPENRESTY_BPFTOOL_NET_VER).tar.gz --strip-components=1 -C openresty-bpftool-net_$(OPENRESTY_BPFTOOL_NET_VER)
	tar -czf openresty-bpftool-net_$(OPENRESTY_BPFTOOL_NET_VER).orig.tar.gz openresty-bpftool-net_$(OPENRESTY_BPFTOOL_NET_VER)

openresty-bpftool-net-clean:
	-cd openresty-bpftool-net && debclean
	-find openresty-bpftool-net -maxdepth 1 ! -name 'debian' ! -name 'openresty-bpftool-net' -print | xargs rm -rf
	rm -rf openresty-bpftool-net*.deb
	rm -rf openresty-bpftool-net_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-bpftool-net-build
openresty-bpftool-net-build: openresty-bpftool-net-clean openresty-bpftool-net-download
	sudo apt-get -y -q install ccache gcc make perl pkg-config openresty-libbpf-net-dev \
		openresty-elfutils-dev openresty-binutils-dev libcap-dev openresty-zlib-dev vim-common
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl pkg-config openresty-libbpf-net-dev \
		openresty-elfutils-dev openresty-binutils-dev libcap-dev openresty-zlib-dev vim-common
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-bpftool-net_$(OPENRESTY_BPFTOOL_NET_VER).orig.tar.gz --strip-components=1 -C openresty-bpftool-net
	cd openresty-bpftool-net \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define distro=$(DISTRO) debian/control.tt2 > debian/control \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
