## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBBPF_NET_VER := 0.4.0.10

deb_toolchain_pkgs=debhelper devscripts

.PHONY: openresty-libbpf-net-download
openresty-libbpf-net-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/libbpf-plus-$(OPENRESTY_LIBBPF_NET_VER).tar.gz ./
	rm -rf openresty-libbpf-net_$(OPENRESTY_LIBBPF_NET_VER)
	mkdir -p openresty-libbpf-net_$(OPENRESTY_LIBBPF_NET_VER)
	tar -xf libbpf-plus-$(OPENRESTY_LIBBPF_NET_VER).tar.gz --strip-components=1 -C openresty-libbpf-net_$(OPENRESTY_LIBBPF_NET_VER)
	tar -czf openresty-libbpf-net_$(OPENRESTY_LIBBPF_NET_VER).orig.tar.gz openresty-libbpf-net_$(OPENRESTY_LIBBPF_NET_VER)

openresty-libbpf-net-clean:
	-cd openresty-libbpf-net && debclean
	-find openresty-libbpf-net -maxdepth 1 ! -name 'debian' ! -name 'openresty-libbpf-net' -print | xargs rm -rf
	rm -rf openresty-libbpf-net*.deb
	rm -rf openresty-libbpf-net_*.*

.PHONY: openresty-libbpf-net-build
openresty-libbpf-net-build: openresty-libbpf-net-clean openresty-libbpf-net-download
	sudo apt-get -y -q install ccache gcc make perl pkg-config openresty-elfutils-dev $(deb_toolchain_pkgs)
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl pkg-config openresty-elfutils-dev $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libbpf-net_$(OPENRESTY_LIBBPF_NET_VER).orig.tar.gz --strip-components=1 -C openresty-libbpf-net
	cd openresty-libbpf-net \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
