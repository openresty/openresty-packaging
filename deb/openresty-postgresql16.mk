## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL16_VER := 16.5

.PHONY: openresty-postgresql16-download
openresty-postgresql16-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://ftp.postgresql.org/pub/source/v$(OPENRESTY_POSTGRESQL16_VER)/postgresql-$(OPENRESTY_POSTGRESQL16_VER).tar.gz'
	rm -rf openresty-postgresql16_$(OPENRESTY_POSTGRESQL16_VER)
	mkdir -p openresty-postgresql16_$(OPENRESTY_POSTGRESQL16_VER)
	tar -xf postgresql-$(OPENRESTY_POSTGRESQL16_VER).tar.gz --strip-components=1 -C openresty-postgresql16_$(OPENRESTY_POSTGRESQL16_VER)
	tar -I 'gzip -1' -cf openresty-postgresql16_$(OPENRESTY_POSTGRESQL16_VER).orig.tar.gz openresty-postgresql16_$(OPENRESTY_POSTGRESQL16_VER)

openresty-postgresql16-clean:
	-cd openresty-postgresql16 && debclean
	-find openresty-postgresql16 -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql16' -print | xargs rm -rf
	rm -rf openresty-postgresql16*.deb
	rm -rf openresty-postgresql16_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-postgresql16-build
openresty-postgresql16-build: openresty-postgresql16-clean openresty-postgresql16-download
	sudo apt-get -y -q install ccache libxml2-dev libxslt-dev libossp-uuid-dev libreadline-dev openresty-plus-openssl111-dev bison libicu-dev pkg-config
	sudo apt-get -y -q install --only-upgrade ccache libxml2-dev libxslt-dev libossp-uuid-dev libreadline-dev openresty-plus-openssl111-dev bison libicu-dev pkg-config
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql16_$(OPENRESTY_POSTGRESQL16_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql16
	cd openresty-postgresql16 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
