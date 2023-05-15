## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_BPFTOOL_VER := 5.13.18.5

.PHONY: openresty-bpftool-download
openresty-bpftool-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/bpftool-plus-$(OPENRESTY_BPFTOOL_VER).tar.gz ./
	rm -rf openresty-bpftool_$(OPENRESTY_BPFTOOL_VER)
	mkdir -p openresty-bpftool_$(OPENRESTY_BPFTOOL_VER)
	tar -xf bpftool-plus-$(OPENRESTY_BPFTOOL_VER).tar.gz --strip-components=1 -C openresty-bpftool_$(OPENRESTY_BPFTOOL_VER)
	tar -czf openresty-bpftool_$(OPENRESTY_BPFTOOL_VER).orig.tar.gz openresty-bpftool_$(OPENRESTY_BPFTOOL_VER)

openresty-bpftool-clean:
	-cd openresty-bpftool && debclean
	-find openresty-bpftool -maxdepth 1 ! -name 'debian' ! -name 'openresty-bpftool' -print | xargs rm -rf
	rm -rf openresty-bpftool*.deb
	rm -rf openresty-bpftool_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-bpftool-build
openresty-bpftool-build: openresty-bpftool-clean openresty-bpftool-download
	sudo apt-get -y -q install ccache gcc make perl pkg-config openresty-libbpf-dev \
		openresty-elfutils-dev openresty-binutils-dev libcap-dev openresty-zlib-dev vim-common
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl pkg-config openresty-libbpf-dev \
		openresty-elfutils-dev openresty-binutils-dev libcap-dev openresty-zlib-dev vim-common
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-bpftool_$(OPENRESTY_BPFTOOL_VER).orig.tar.gz --strip-components=1 -C openresty-bpftool
	cd openresty-bpftool \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define distro=$(DISTRO) debian/control.tt2 > debian/control \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
