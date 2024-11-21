## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL15_VER := 15.9

.PHONY: openresty-postgresql15-download
openresty-postgresql15-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://ftp.postgresql.org/pub/source/v$(OPENRESTY_POSTGRESQL15_VER)/postgresql-$(OPENRESTY_POSTGRESQL15_VER).tar.gz'
	rm -rf openresty-postgresql15_$(OPENRESTY_POSTGRESQL15_VER)
	mkdir -p openresty-postgresql15_$(OPENRESTY_POSTGRESQL15_VER)
	tar -xf postgresql-$(OPENRESTY_POSTGRESQL15_VER).tar.gz --strip-components=1 -C openresty-postgresql15_$(OPENRESTY_POSTGRESQL15_VER)
	tar -czf openresty-postgresql15_$(OPENRESTY_POSTGRESQL15_VER).orig.tar.gz openresty-postgresql15_$(OPENRESTY_POSTGRESQL15_VER)

openresty-postgresql15-clean:
	-cd openresty-postgresql15 && debclean
	-find openresty-postgresql15 -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql15' -print | xargs rm -rf
	rm -rf openresty-postgresql15*.deb
	rm -rf openresty-postgresql15_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-postgresql15-build
openresty-postgresql15-build: openresty-postgresql15-clean openresty-postgresql15-download
	sudo apt-get -y -q install ccache libxml2-dev libxslt-dev libossp-uuid-dev libreadline-dev openresty-plus-openssl111-dev libicu-dev bison pkg-config
	sudo apt-get -y -q install --only-upgrade ccache libxml2-dev libxslt-dev libossp-uuid-dev libreadline-dev openresty-plus-openssl111-dev libicu-dev bison pkg-config
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql15_$(OPENRESTY_POSTGRESQL15_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql15
	cd openresty-postgresql15 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
