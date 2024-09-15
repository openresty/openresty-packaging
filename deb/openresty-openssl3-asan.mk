## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_OPENSSL3_VER := 3.0.15

.PHONY: openresty-openssl3-asan-download
openresty-openssl3-asan-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/openssl/openssl/releases/download/openssl-$(OPENRESTY_OPENSSL3_VER)/openssl-$(OPENRESTY_OPENSSL3_VER).tar.gz'
	rm -rf openresty-openssl3-asan_$(OPENRESTY_OPENSSL3_VER)
	mkdir -p openresty-openssl3-asan_$(OPENRESTY_OPENSSL3_VER)
	tar -xf openssl-$(OPENRESTY_OPENSSL3_VER).tar.gz --strip-components=1 -C openresty-openssl3-asan_$(OPENRESTY_OPENSSL3_VER)
	tar -czf openresty-openssl3-asan_$(OPENRESTY_OPENSSL3_VER).orig.tar.gz openresty-openssl3-asan_$(OPENRESTY_OPENSSL3_VER)

openresty-openssl3-asan-clean:
	-cd openresty-openssl3-asan && debclean
	-find openresty-openssl3-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-openssl3-asan' -print | xargs rm -rf
	rm -rf openresty-openssl3-asan*.deb
	rm -rf openresty-openssl3-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-openssl3-asan-build
openresty-openssl3-asan-build: openresty-openssl3-asan-clean openresty-openssl3-asan-download
	sudo apt-get -y -q install gcc make perl openresty-zlib-dev
	sudo apt-get -y -q install --only-upgrade gcc make perl openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl3-asan_$(OPENRESTY_OPENSSL3_VER).orig.tar.gz --strip-components=1 -C openresty-openssl3-asan
	cd openresty-openssl3-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
