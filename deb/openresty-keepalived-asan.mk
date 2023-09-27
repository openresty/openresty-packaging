## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_KEEPALIVED_ASAN_VER := 2.2.4

.PHONY: openresty-keepalived-asan-download
openresty-keepalived-asan-download:
	wget -nH --cut-dirs=100 --mirror 'https://www.keepalived.org/software/keepalived-$(OPENRESTY_KEEPALIVED_ASAN_VER).tar.gz'
	rm -rf openresty-keepalived-asan_$(OPENRESTY_KEEPALIVED_ASAN_VER)
	mkdir -p openresty-keepalived-asan_$(OPENRESTY_KEEPALIVED_ASAN_VER)
	tar -xf keepalived-$(OPENRESTY_KEEPALIVED_ASAN_VER).tar.gz --strip-components=1 -C openresty-keepalived-asan_$(OPENRESTY_KEEPALIVED_ASAN_VER)
	tar -czf openresty-keepalived-asan_$(OPENRESTY_KEEPALIVED_ASAN_VER).orig.tar.gz openresty-keepalived-asan_$(OPENRESTY_KEEPALIVED_ASAN_VER)

openresty-keepalived-asan-clean:
	-cd openresty-keepalived-asan && debclean
	-find openresty-keepalived-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-keepalived-asan' -print | xargs rm -rf
	rm -rf openresty-keepalived-asan*.deb
	rm -rf openresty-keepalived-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-keepalived-asan-build
openresty-keepalived-asan-build: openresty-keepalived-asan-clean openresty-keepalived-asan-download
	sudo apt-get -y -q install build-essential pkg-config automake autoconf ccache gcc make openresty-plus-openssl111-dev libnl-genl-3-dev libnl-3-dev
	sudo apt-get -y -q install --only-upgrade build-essential pkg-config automake autoconf ccache gcc make openresty-plus-openssl111-dev libnl-genl-3-dev libnl-3-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-keepalived-asan_$(OPENRESTY_KEEPALIVED_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-keepalived-asan
	cd openresty-keepalived-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
