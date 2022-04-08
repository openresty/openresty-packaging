## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_CYRUS_SASL_VER := 2.1.28

.PHONY: openresty-cyrus-sasl-download
openresty-cyrus-sasl-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/cyrusimap/cyrus-sasl/archive/cyrus-sasl-$(OPENRESTY_CYRUS_SASL_VER).tar.gz'
	rm -rf openresty-cyrus-sasl_$(OPENRESTY_CYRUS_SASL_VER)
	mkdir -p openresty-cyrus-sasl_$(OPENRESTY_CYRUS_SASL_VER)
	tar -xf cyrus-sasl-$(OPENRESTY_CYRUS_SASL_VER).tar.gz --strip-components=1 -C openresty-cyrus-sasl_$(OPENRESTY_CYRUS_SASL_VER)
	tar -czf openresty-cyrus-sasl_$(OPENRESTY_CYRUS_SASL_VER).orig.tar.gz openresty-cyrus-sasl_$(OPENRESTY_CYRUS_SASL_VER)

openresty-cyrus-sasl-clean:
	-cd openresty-cyrus-sasl && debclean
	-find openresty-cyrus-sasl -maxdepth 1 ! -name 'debian' ! -name 'openresty-cyrus-sasl' -print | xargs rm -rf
	rm -rf openresty-cyrus-sasl*.deb
	rm -rf openresty-cyrus-sasl_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-cyrus-sasl-build
openresty-cyrus-sasl-build: openresty-cyrus-sasl-clean openresty-cyrus-sasl-download
	sudo apt-get -y -q install libtool openresty-plus-openssl111
	sudo apt-get -y -q install --only-upgrade libtool openresty-plus-openssl111
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-cyrus-sasl_$(OPENRESTY_CYRUS_SASL_VER).orig.tar.gz --strip-components=1 -C openresty-cyrus-sasl
	cd openresty-cyrus-sasl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
