## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL_TIMESCALEDB_VER := 1.7.4

.PHONY: openresty-postgresql-timescaledb-download
openresty-postgresql-timescaledb-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/timescale/timescaledb/archive/$(OPENRESTY_POSTGRESQL_TIMESCALEDB_VER).tar.gz'
	rm -rf openresty-postgresql-timescaledb_$(OPENRESTY_POSTGRESQL_TIMESCALEDB_VER)
	mkdir -p openresty-postgresql-timescaledb_$(OPENRESTY_POSTGRESQL_TIMESCALEDB_VER)
	tar -xf $(OPENRESTY_POSTGRESQL_TIMESCALEDB_VER).tar.gz --strip-components=1 -C openresty-postgresql-timescaledb_$(OPENRESTY_POSTGRESQL_TIMESCALEDB_VER)
	tar -I 'gzip -1' -cf openresty-postgresql-timescaledb_$(OPENRESTY_POSTGRESQL_TIMESCALEDB_VER).orig.tar.gz openresty-postgresql-timescaledb_$(OPENRESTY_POSTGRESQL_TIMESCALEDB_VER)

openresty-postgresql-timescaledb-clean:
	-cd openresty-postgresql-timescaledb && debclean
	-find openresty-postgresql-timescaledb -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql-timescaledb' -print | xargs rm -rf
	rm -rf openresty-postgresql-timescaledb*.deb
	rm -rf openresty-postgresql-timescaledb_*.*

.PHONY: openresty-postgresql-timescaledb-build
openresty-postgresql-timescaledb-build: openresty-postgresql-timescaledb-clean openresty-postgresql-timescaledb-download
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes -y -q install openresty-postgresql-dev openresty-plus-openssl111-dev
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes --only-upgrade -y -q install openresty-postgresql-dev openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql-timescaledb_$(OPENRESTY_POSTGRESQL_TIMESCALEDB_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql-timescaledb
	cd openresty-postgresql-timescaledb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
