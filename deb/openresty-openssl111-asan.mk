## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_OPENSSL111_ASAN_VER := 1.1.1l

.PHONY: openresty-openssl111-asan-download
openresty-openssl111-asan-download:
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(OPENRESTY_OPENSSL111_ASAN_VER).tar.gz'
	rm -rf openresty-openssl111-asan_$(OPENRESTY_OPENSSL111_ASAN_VER)
	mkdir -p openresty-openssl111-asan_$(OPENRESTY_OPENSSL111_ASAN_VER)
	tar -xf openssl-$(OPENRESTY_OPENSSL111_ASAN_VER).tar.gz --strip-components=1 -C openresty-openssl111-asan_$(OPENRESTY_OPENSSL111_ASAN_VER)
	tar -czf openresty-openssl111-asan_$(OPENRESTY_OPENSSL111_ASAN_VER).orig.tar.gz openresty-openssl111-asan_$(OPENRESTY_OPENSSL111_ASAN_VER)

openresty-openssl111-asan-clean:
	-cd openresty-openssl111-asan && debclean
	-find openresty-openssl111-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-openssl111-asan' -print | xargs rm -rf
	rm -rf openresty-openssl111-asan*.deb
	rm -rf openresty-openssl111-asan_*.*

.PHONY: openresty-openssl111-asan-build
openresty-openssl111-asan-build: openresty-openssl111-asan-clean openresty-openssl111-asan-download
	sudo apt-get -y -q install ccache make perl gcc openresty-zlib-asan-dev
	sudo apt-get -y -q install --only-upgrade ccache make perl gcc openresty-zlib-asan-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl111-asan_$(OPENRESTY_OPENSSL111_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-openssl111-asan
	cd openresty-openssl111-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
