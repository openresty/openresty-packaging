## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_IPROUTE2_VER := 6.3.0

.PHONY: openresty-iproute2-download
openresty-iproute2-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'http://kernel.org/pub/linux/utils/net/iproute2/iproute2-$(OPENRESTY_IPROUTE2_VER).tar.xz'
	rm -rf openresty-iproute2_$(OPENRESTY_IPROUTE2_VER)
	mkdir -p openresty-iproute2_$(OPENRESTY_IPROUTE2_VER)
	tar -xf iproute2-$(OPENRESTY_IPROUTE2_VER).tar.xz --strip-components=1 -C openresty-iproute2_$(OPENRESTY_IPROUTE2_VER)
	tar -czf openresty-iproute2_$(OPENRESTY_IPROUTE2_VER).orig.tar.gz openresty-iproute2_$(OPENRESTY_IPROUTE2_VER)

openresty-iproute2-clean:
	-cd openresty-iproute2 && debclean
	-find openresty-iproute2 -maxdepth 1 ! -name 'debian' ! -name 'openresty-iproute2' -print | xargs rm -rf
	rm -rf openresty-iproute2*.deb
	rm -rf openresty-iproute2_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-iproute2-build
openresty-iproute2-build: openresty-iproute2-clean openresty-iproute2-download
	sudo apt-get -y -q install bison flex libdb-dev libmnl-dev pkg-config ccache patch openresty-elfutils-dev openresty-libbpf-net-dev zlib1g-dev
	sudo apt-get -y -q install --only-upgrade bison flex libdb-dev libmnl-dev pkg-config ccache patch openresty-elfutils-dev openresty-libbpf-net-dev zlib1g-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-iproute2_$(OPENRESTY_IPROUTE2_VER).orig.tar.gz --strip-components=1 -C openresty-iproute2
	cd openresty-iproute2 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
