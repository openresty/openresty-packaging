## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ASAN_VER := 1.19.3.1

.PHONY: openresty-asan-download
openresty-asan-download:
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-$(OPENRESTY_ASAN_VER).tar.gz'
	rm -rf openresty-asan_$(OPENRESTY_ASAN_VER)
	mkdir -p openresty-asan_$(OPENRESTY_ASAN_VER)
	tar -xf openresty-$(OPENRESTY_ASAN_VER).tar.gz --strip-components=1 -C openresty-asan_$(OPENRESTY_ASAN_VER)
	tar -czf openresty-asan_$(OPENRESTY_ASAN_VER).orig.tar.gz openresty-asan_$(OPENRESTY_ASAN_VER)

openresty-asan-clean:
	-cd openresty-asan && debclean
	-find openresty-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-asan' -print | xargs rm -rf
	rm -rf openresty-asan*.deb
	rm -rf openresty-asan_*.*

.PHONY: openresty-asan-build
openresty-asan-build: openresty-asan-clean openresty-asan-download
	sudo apt-get -y -q install ccache make perl systemtap-sdt-dev gcc valgrind openresty-zlib-asan-dev openresty-openssl111-asan-dev openresty-pcre-asan-dev
	sudo apt-get -y -q install --only-upgrade ccache make perl systemtap-sdt-dev gcc valgrind openresty-zlib-asan-dev openresty-openssl111-asan-dev openresty-pcre-asan-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-asan_$(OPENRESTY_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-asan
	cd openresty-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
