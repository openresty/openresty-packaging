## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBRDKAFKA_VER := 2.4.0

.PHONY: openresty-librdkafka-download
openresty-librdkafka-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/confluentinc/librdkafka/archive/refs/tags/v$(OPENRESTY_LIBRDKAFKA_VER).tar.gz'
	rm -rf openresty-librdkafka_$(OPENRESTY_LIBRDKAFKA_VER)
	mkdir -p openresty-librdkafka_$(OPENRESTY_LIBRDKAFKA_VER)
	tar -xf v$(OPENRESTY_LIBRDKAFKA_VER).tar.gz --strip-components=1 -C openresty-librdkafka_$(OPENRESTY_LIBRDKAFKA_VER)
	rm -fr openresty-librdkafka_$(OPENRESTY_LIBRDKAFKA_VER)/debian
	tar -czf openresty-librdkafka_$(OPENRESTY_LIBRDKAFKA_VER).orig.tar.gz openresty-librdkafka_$(OPENRESTY_LIBRDKAFKA_VER)

openresty-librdkafka-clean:
	-cd openresty-librdkafka && debclean
	-find openresty-librdkafka -maxdepth 1 ! -name 'debian' ! -name 'openresty-librdkafka' -print | xargs rm -rf
	rm -rf openresty-librdkafka*.deb
	rm -rf openresty-librdkafka_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-librdkafka-build
openresty-librdkafka-build: openresty-librdkafka-clean openresty-librdkafka-download
	sudo apt-get -y -q install libtool openresty-openssl111-dev openresty-cyrus-sasl-dev
	sudo apt-get -y -q install --only-upgrade libtool openresty-openssl111-dev openresty-cyrus-sasl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-librdkafka_$(OPENRESTY_LIBRDKAFKA_VER).orig.tar.gz --strip-components=1 -C openresty-librdkafka
	cd openresty-librdkafka \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
