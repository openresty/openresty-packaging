## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_XDP_TOOLS_VER := 1.2.2.1
os_arch = $(shell arch)
arch_asm = /usr/include/$(os_arch)-linux-gnu/asm

X64_DEP_LIBS =
ifeq ($(ARCH), amd64)
X64_DEP_LIBS = gcc-multilib
endif

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
	if [ -e $(arch_asm) ] && [ ! -e /usr/include/asm ]; then ln -s $(arch_asm) /usr/include/asm; fi
	sudo apt-get -y -q install ccache gcc make perl pkg-config openresty-libbpf-net-dev openresty-pcap-dev openresty-elfutils-dev openresty-llvm zlib1g-dev $(X64_DEP_LIBS)
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl pkg-config openresty-libbpf-net-dev openresty-pcap-dev openresty-elfutils-dev openresty-llvm zlib1g-dev $(X64_DEP_LIBS)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	if [ "$(ARCH)" == "arm64" ] && [ ! -e /usr/include/asm ]; then sudo ln -s /usr/include/`uname -m`-linux-gnu/asm /usr/include/asm; fi
	tar xf openresty-xdp-tools_$(OPENRESTY_XDP_TOOLS_VER).orig.tar.gz --strip-components=1 -C openresty-xdp-tools
	cd openresty-xdp-tools \
		&& tpage --define arch=$(ARCH) --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define arch=$(ARCH) --define distro=$(DISTRO) debian/control.tt2 > debian/control \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
