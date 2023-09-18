## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SAAS_ZLIB_ASAN_VER := 1.3

.PHONY: openresty-saas-zlib-asan-download
openresty-saas-zlib-asan-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'http://www.zlib.net/zlib-$(OPENRESTY_SAAS_ZLIB_ASAN_VER).tar.xz'
	rm -rf openresty-saas-zlib-asan_$(OPENRESTY_SAAS_ZLIB_ASAN_VER)
	mkdir -p openresty-saas-zlib-asan_$(OPENRESTY_SAAS_ZLIB_ASAN_VER)
	tar -xf zlib-$(OPENRESTY_SAAS_ZLIB_ASAN_VER).tar.xz --strip-components=1 -C openresty-saas-zlib-asan_$(OPENRESTY_SAAS_ZLIB_ASAN_VER)
	tar -czf openresty-saas-zlib-asan_$(OPENRESTY_SAAS_ZLIB_ASAN_VER).orig.tar.gz openresty-saas-zlib-asan_$(OPENRESTY_SAAS_ZLIB_ASAN_VER)

openresty-saas-zlib-asan-clean:
	-cd openresty-saas-zlib-asan && debclean
	-find openresty-saas-zlib-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-saas-zlib-asan' -print | xargs rm -rf
	rm -rf openresty-saas-zlib-asan*.deb
	rm -rf openresty-saas-zlib-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-saas-zlib-asan-build
openresty-saas-zlib-asan-build: openresty-saas-zlib-asan-clean openresty-saas-zlib-asan-download
	sudo apt-get -y -q install libtool
	sudo apt-get -y -q install --only-upgrade libtool
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-saas-zlib-asan_$(OPENRESTY_SAAS_ZLIB_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-saas-zlib-asan
	cd openresty-saas-zlib-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
