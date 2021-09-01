## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PLUS_OPENSSL111_ASAN_VER := 1.1.1l

.PHONY: openresty-plus-openssl111-asan-download
openresty-plus-openssl111-asan-download:
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(OPENRESTY_PLUS_OPENSSL111_ASAN_VER).tar.gz'
	rm -rf openresty-plus-openssl111-asan_$(OPENRESTY_PLUS_OPENSSL111_ASAN_VER)
	mkdir -p openresty-plus-openssl111-asan_$(OPENRESTY_PLUS_OPENSSL111_ASAN_VER)
	tar -xf openssl-$(OPENRESTY_PLUS_OPENSSL111_ASAN_VER).tar.gz --strip-components=1 -C openresty-plus-openssl111-asan_$(OPENRESTY_PLUS_OPENSSL111_ASAN_VER)
	tar -czf openresty-plus-openssl111-asan_$(OPENRESTY_PLUS_OPENSSL111_ASAN_VER).orig.tar.gz openresty-plus-openssl111-asan_$(OPENRESTY_PLUS_OPENSSL111_ASAN_VER)

openresty-plus-openssl111-asan-clean:
	-cd openresty-plus-openssl111-asan && debclean
	-find openresty-plus-openssl111-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-openssl111-asan' -print | xargs rm -rf
	rm -rf openresty-plus-openssl111-asan*.deb
	rm -rf openresty-plus-openssl111-asan_*.*

.PHONY: openresty-plus-openssl111-asan-build
openresty-plus-openssl111-asan-build: openresty-plus-openssl111-asan-clean openresty-plus-openssl111-asan-download
	sudo apt-get -y -q install ccache gcc make perl openresty-zlib-asan-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl openresty-zlib-asan-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-openssl111-asan_$(OPENRESTY_PLUS_OPENSSL111_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-plus-openssl111-asan
	cd openresty-plus-openssl111-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
