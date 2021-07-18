## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBBPF_VER := 0.4.0.2

deb_toolchain_pkgs=debhelper devscripts

.PHONY: openresty-libbpf-download
openresty-libbpf-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/libbpf-plus-$(OPENRESTY_LIBBPF_VER).tar.gz ./
	rm -rf openresty-libbpf_$(OPENRESTY_LIBBPF_VER)
	mkdir -p openresty-libbpf_$(OPENRESTY_LIBBPF_VER)
	tar -xf libbpf-plus-$(OPENRESTY_LIBBPF_VER).tar.gz --strip-components=1 -C openresty-libbpf_$(OPENRESTY_LIBBPF_VER)
	tar -czf openresty-libbpf_$(OPENRESTY_LIBBPF_VER).orig.tar.gz openresty-libbpf_$(OPENRESTY_LIBBPF_VER)

openresty-libbpf-clean:
	-cd openresty-libbpf && debclean
	-find openresty-libbpf -maxdepth 1 ! -name 'debian' ! -name 'openresty-libbpf' -print | xargs rm -rf
	rm -rf openresty-libbpf*.deb
	rm -rf openresty-libbpf_*.*

.PHONY: openresty-libbpf-build
openresty-libbpf-build: openresty-libbpf-clean openresty-libbpf-download
	sudo apt-get -y -q install ccache gcc make perl pkg-config openresty-elfutils-dev $(deb_toolchain_pkgs)
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl pkg-config openresty-elfutils-dev $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libbpf_$(OPENRESTY_LIBBPF_VER).orig.tar.gz --strip-components=1 -C openresty-libbpf
	cd openresty-libbpf \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
