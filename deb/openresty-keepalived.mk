## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_KEEPALIVED_VER := 2.2.4

.PHONY: openresty-keepalived-download
openresty-keepalived-download:
	wget -nH --cut-dirs=100 --mirror 'https://www.keepalived.org/software/keepalived-$(OPENRESTY_KEEPALIVED_VER).tar.gz'
	rm -rf openresty-keepalived_$(OPENRESTY_KEEPALIVED_VER)
	mkdir -p openresty-keepalived_$(OPENRESTY_KEEPALIVED_VER)
	tar -xf keepalived-$(OPENRESTY_KEEPALIVED_VER).tar.gz --strip-components=1 -C openresty-keepalived_$(OPENRESTY_KEEPALIVED_VER)
	tar -czf openresty-keepalived_$(OPENRESTY_KEEPALIVED_VER).orig.tar.gz openresty-keepalived_$(OPENRESTY_KEEPALIVED_VER)

openresty-keepalived-clean:
	-cd openresty-keepalived && debclean
	-find openresty-keepalived -maxdepth 1 ! -name 'debian' ! -name 'openresty-keepalived' -print | xargs rm -rf
	rm -rf openresty-keepalived*.deb
	rm -rf openresty-keepalived_*.*

.PHONY: openresty-keepalived-build
openresty-keepalived-build: openresty-keepalived-clean openresty-keepalived-download
	sudo apt-get -y -q install build-essential pkg-config automake autoconf ccache gcc make openresty-plus-openssl111-dev libnl-genl-3-dev libnl-3-dev
	sudo apt-get -y -q install --only-upgrade build-essential pkg-config automake autoconf ccache gcc make openresty-plus-openssl111-dev libnl-genl-3-dev libnl-3-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-keepalived_$(OPENRESTY_KEEPALIVED_VER).orig.tar.gz --strip-components=1 -C openresty-keepalived
	cd openresty-keepalived \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
