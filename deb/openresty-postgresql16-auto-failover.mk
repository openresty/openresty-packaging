## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER := 2.1

.PHONY: openresty-postgresql16-auto-failover-download
openresty-postgresql16-auto-failover-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/citusdata/pg_auto_failover/archive/v$(OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER).tar.gz'
	rm -rf openresty-postgresql16-auto-failover_$(OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER)
	mkdir -p openresty-postgresql16-auto-failover_$(OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER)
	tar -xf v$(OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER).tar.gz --strip-components=1 -C openresty-postgresql16-auto-failover_$(OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER)
	tar -czf openresty-postgresql16-auto-failover_$(OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER).orig.tar.gz openresty-postgresql16-auto-failover_$(OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER)

openresty-postgresql16-auto-failover-clean:
	-cd openresty-postgresql16-auto-failover && debclean
	-find openresty-postgresql16-auto-failover -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql16-auto-failover' -print | xargs rm -rf
	rm -rf openresty-postgresql16-auto-failover*.deb
	rm -rf openresty-postgresql16-auto-failover_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-postgresql16-auto-failover-build
openresty-postgresql16-auto-failover-build: openresty-postgresql16-auto-failover-clean openresty-postgresql16-auto-failover-download
	sudo apt-get -y -q install openresty-postgresql16-dev ccache ncurses-dev libxml2-dev libxslt-dev libreadline-dev zlib1g-dev make gcc
	sudo apt-get -y -q install --only-upgrade openresty-postgresql16-dev ccache ncurses-dev libxml2-dev libxslt-dev libreadline-dev zlib1g-dev make gcc
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql16-auto-failover_$(OPENRESTY_POSTGRESQL16_AUTO_FAILOVER_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql16-auto-failover
	cd openresty-postgresql16-auto-failover \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
