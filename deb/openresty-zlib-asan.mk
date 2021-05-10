## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ZLIB_ASAN_VER := 1.2.11

.PHONY: openresty-zlib-asan-download
openresty-zlib-asan-download:
	wget -nH --cut-dirs=100 --mirror 'http://www.zlib.net/zlib-$(OPENRESTY_ZLIB_ASAN_VER).tar.xz'
	rm -rf openresty-zlib-asan_$(OPENRESTY_ZLIB_ASAN_VER)
	mkdir -p openresty-zlib-asan_$(OPENRESTY_ZLIB_ASAN_VER)
	tar -xf zlib-$(OPENRESTY_ZLIB_ASAN_VER).tar.xz --strip-components=1 -C openresty-zlib-asan_$(OPENRESTY_ZLIB_ASAN_VER)
	tar -czf openresty-zlib-asan_$(OPENRESTY_ZLIB_ASAN_VER).orig.tar.gz openresty-zlib-asan_$(OPENRESTY_ZLIB_ASAN_VER)

openresty-zlib-asan-clean:
	-cd openresty-zlib-asan && debclean
	-find openresty-zlib-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-zlib-asan' -print | xargs rm -rf
	rm -rf openresty-zlib-asan*.deb
	rm -rf openresty-zlib-asan_*.*

.PHONY: openresty-zlib-asan-build
openresty-zlib-asan-build: openresty-zlib-asan-clean openresty-zlib-asan-download
	sudo apt-get -y -q install libtool gcc
	sudo apt-get -y -q install --only-upgrade libtool gcc
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-zlib-asan_$(OPENRESTY_ZLIB_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-zlib-asan
	cd openresty-zlib-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
