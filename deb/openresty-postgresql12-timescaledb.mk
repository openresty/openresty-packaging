## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER := 1.7.4

.PHONY: openresty-postgresql12-timescaledb-download
openresty-postgresql12-timescaledb-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/timescale/timescaledb/archive/$(OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER).tar.gz'
	rm -rf openresty-postgresql12-timescaledb_$(OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER)
	mkdir -p openresty-postgresql12-timescaledb_$(OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER)
	tar -xf $(OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER).tar.gz --strip-components=1 -C openresty-postgresql12-timescaledb_$(OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER)
	tar -I 'gzip -1' -cf openresty-postgresql12-timescaledb_$(OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER).orig.tar.gz openresty-postgresql12-timescaledb_$(OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER)

openresty-postgresql12-timescaledb-clean:
	-cd openresty-postgresql12-timescaledb && debclean
	-find openresty-postgresql12-timescaledb -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql12-timescaledb' -print | xargs rm -rf
	rm -rf openresty-postgresql12-timescaledb*.deb
	rm -rf openresty-postgresql12-timescaledb_*.*

.PHONY: openresty-postgresql12-timescaledb-build
openresty-postgresql12-timescaledb-build: openresty-postgresql12-timescaledb-clean openresty-postgresql12-timescaledb-download
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes -y -q install openresty-postgresql12-dev openresty-plus-openssl111-dev
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes --only-upgrade -y -q install openresty-postgresql12-dev openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql12-timescaledb_$(OPENRESTY_POSTGRESQL12_TIMESCALEDB_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql12-timescaledb
	cd openresty-postgresql12-timescaledb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
