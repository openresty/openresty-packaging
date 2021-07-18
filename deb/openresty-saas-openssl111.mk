## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SAAS_OPENSSL111_VER := 1.1.1k

.PHONY: openresty-saas-openssl111-download
openresty-saas-openssl111-download:
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(OPENRESTY_SAAS_OPENSSL111_VER).tar.gz'
	rm -rf openresty-saas-openssl111_$(OPENRESTY_SAAS_OPENSSL111_VER)
	mkdir -p openresty-saas-openssl111_$(OPENRESTY_SAAS_OPENSSL111_VER)
	tar -xf openssl-$(OPENRESTY_SAAS_OPENSSL111_VER).tar.gz --strip-components=1 -C openresty-saas-openssl111_$(OPENRESTY_SAAS_OPENSSL111_VER)
	tar -czf openresty-saas-openssl111_$(OPENRESTY_SAAS_OPENSSL111_VER).orig.tar.gz openresty-saas-openssl111_$(OPENRESTY_SAAS_OPENSSL111_VER)

openresty-saas-openssl111-clean:
	cd openresty-saas-openssl111 && debclean
	-find openresty-saas-openssl111 -maxdepth 1 ! -name 'debian' ! -name 'openresty-saas-openssl111' -print | xargs rm -rf
	rm -rf openresty-saas-openssl111*.deb
	rm -rf openresty-saas-openssl111_*.*

.PHONY: openresty-saas-openssl111-build
openresty-saas-openssl111-build: openresty-saas-openssl111-clean openresty-saas-openssl111-download
	sudo apt-get -y -q install gcc make perl openresty-saas-zlib-dev
	sudo apt-get -y -q --only-upgrade install gcc make perl openresty-saas-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-saas-openssl111_$(OPENRESTY_SAAS_OPENSSL111_VER).orig.tar.gz --strip-components=1 -C openresty-saas-openssl111
	cd openresty-saas-openssl111 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
