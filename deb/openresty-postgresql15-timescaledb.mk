## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER := 2.10.3

.PHONY: openresty-postgresql15-timescaledb-download
openresty-postgresql15-timescaledb-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/timescale/timescaledb/archive/$(OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER).tar.gz'
	rm -rf openresty-postgresql15-timescaledb_$(OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER)
	mkdir -p openresty-postgresql15-timescaledb_$(OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER)
	tar -xf $(OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER).tar.gz --strip-components=1 -C openresty-postgresql15-timescaledb_$(OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER)
	tar -I 'gzip -1' -cf openresty-postgresql15-timescaledb_$(OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER).orig.tar.gz openresty-postgresql15-timescaledb_$(OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER)

openresty-postgresql15-timescaledb-clean:
	-cd openresty-postgresql15-timescaledb && debclean
	-find openresty-postgresql15-timescaledb -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql15-timescaledb' -print | xargs rm -rf
	rm -rf openresty-postgresql15-timescaledb*.deb
	rm -rf openresty-postgresql15-timescaledb_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-postgresql15-timescaledb-build
openresty-postgresql15-timescaledb-build: openresty-postgresql15-timescaledb-clean openresty-postgresql15-timescaledb-download
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes -y -q install openresty-postgresql15-dev openresty-plus-openssl111-dev cmake
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes --only-upgrade -y -q install openresty-postgresql15-dev openresty-plus-openssl111-dev cmake
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql15-timescaledb_$(OPENRESTY_POSTGRESQL15_TIMESCALEDB_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql15-timescaledb
	cd openresty-postgresql15-timescaledb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
