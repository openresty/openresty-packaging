## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SAAS_OPENSSL111_ASAN_VER := $(SSL111_VER)

.PHONY: openresty-saas-openssl111-asan-download
openresty-saas-openssl111-asan-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(OPENRESTY_SAAS_OPENSSL111_ASAN_VER).tar.gz'
	rm -rf openresty-saas-openssl111-asan_$(OPENRESTY_SAAS_OPENSSL111_ASAN_VER)
	mkdir -p openresty-saas-openssl111-asan_$(OPENRESTY_SAAS_OPENSSL111_ASAN_VER)
	tar -xf openssl-$(OPENRESTY_SAAS_OPENSSL111_ASAN_VER).tar.gz --strip-components=1 -C openresty-saas-openssl111-asan_$(OPENRESTY_SAAS_OPENSSL111_ASAN_VER)
	tar -czf openresty-saas-openssl111-asan_$(OPENRESTY_SAAS_OPENSSL111_ASAN_VER).orig.tar.gz openresty-saas-openssl111-asan_$(OPENRESTY_SAAS_OPENSSL111_ASAN_VER)

openresty-saas-openssl111-asan-clean:
	-cd openresty-saas-openssl111-asan && debclean
	-find openresty-saas-openssl111-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-saas-openssl111-asan' -print | xargs rm -rf
	rm -rf openresty-saas-openssl111-asan*.deb
	rm -rf openresty-saas-openssl111-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-saas-openssl111-asan-build
openresty-saas-openssl111-asan-build: openresty-saas-openssl111-asan-clean openresty-saas-openssl111-asan-download
	sudo apt-get -y -q install gcc make perl openresty-saas-zlib-dev
	sudo apt-get -y -q install --only-upgrade gcc make perl openresty-saas-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-saas-openssl111-asan_$(OPENRESTY_SAAS_OPENSSL111_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-saas-openssl111-asan
	cd openresty-saas-openssl111-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
