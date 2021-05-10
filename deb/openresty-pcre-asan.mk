## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PCRE_ASAN_VER := 8.44

.PHONY: openresty-pcre-asan-download
openresty-pcre-asan-download:
	wget -nH --cut-dirs=100 --mirror 'https://ftp.pcre.org/pub/pcre/pcre-$(OPENRESTY_PCRE_ASAN_VER).tar.bz2'
	rm -rf openresty-pcre-asan_$(OPENRESTY_PCRE_ASAN_VER)
	mkdir -p openresty-pcre-asan_$(OPENRESTY_PCRE_ASAN_VER)
	tar -xf pcre-$(OPENRESTY_PCRE_ASAN_VER).tar.bz2 --strip-components=1 -C openresty-pcre-asan_$(OPENRESTY_PCRE_ASAN_VER)
	tar -czf openresty-pcre-asan_$(OPENRESTY_PCRE_ASAN_VER).orig.tar.gz openresty-pcre-asan_$(OPENRESTY_PCRE_ASAN_VER)

openresty-pcre-asan-clean:
	-cd openresty-pcre-asan && debclean
	-find openresty-pcre-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-pcre-asan' -print | xargs rm -rf
	rm -rf openresty-pcre-asan*.deb
	rm -rf openresty-pcre-asan_*.*

.PHONY: openresty-pcre-asan-build
openresty-pcre-asan-build: openresty-pcre-asan-clean openresty-pcre-asan-download
	sudo apt-get -y -q install ccache libtool gcc
	sudo apt-get -y -q install --only-upgrade ccache libtool gcc
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-pcre-asan_$(OPENRESTY_PCRE_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-pcre-asan
	cd openresty-pcre-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
