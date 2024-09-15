## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_OPENSSL30_VER := 3.0.15

.PHONY: openresty-openssl30-download
openresty-openssl30-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/openssl/openssl/releases/download/openssl-$(OPENRESTY_OPENSSL30_VER)/openssl-$(OPENRESTY_OPENSSL30_VER).tar.gz'
	rm -rf openresty-openssl30_$(OPENRESTY_OPENSSL30_VER)
	mkdir -p openresty-openssl30_$(OPENRESTY_OPENSSL30_VER)
	tar -xf openssl-$(OPENRESTY_OPENSSL30_VER).tar.gz --strip-components=1 -C openresty-openssl30_$(OPENRESTY_OPENSSL30_VER)
	tar -czf openresty-openssl30_$(OPENRESTY_OPENSSL30_VER).orig.tar.gz openresty-openssl30_$(OPENRESTY_OPENSSL30_VER)

openresty-openssl30-clean:
	-cd openresty-openssl30 && debclean
	-find openresty-openssl30 -maxdepth 1 ! -name 'debian' ! -name 'openresty-openssl30' -print | xargs rm -rf
	rm -rf openresty-openssl30*.deb
	rm -rf openresty-openssl30_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-openssl30-build
openresty-openssl30-build: openresty-openssl30-clean openresty-openssl30-download
	sudo apt-get -y -q install gcc make perl openresty-zlib-dev
	sudo apt-get -y -q install --only-upgrade gcc make perl openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl30_$(OPENRESTY_OPENSSL30_VER).orig.tar.gz --strip-components=1 -C openresty-openssl30
	cd openresty-openssl30 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
