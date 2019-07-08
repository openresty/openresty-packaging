## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL_IP4R_VER := 2.4.1

.PHONY: openresty-postgresql-ip4r-download
openresty-postgresql-ip4r-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/RhodiumToad/ip4r/archive/$(OPENRESTY_POSTGRESQL_IP4R_VER).tar.gz'
	rm -rf openresty-postgresql-ip4r_$(OPENRESTY_POSTGRESQL_IP4R_VER)
	mkdir -p openresty-postgresql-ip4r_$(OPENRESTY_POSTGRESQL_IP4R_VER)
	tar -xf 2.4.1.tar.gz --strip-components=1 -C openresty-postgresql-ip4r_$(OPENRESTY_POSTGRESQL_IP4R_VER)
	tar -czf openresty-postgresql-ip4r_$(OPENRESTY_POSTGRESQL_IP4R_VER).orig.tar.gz openresty-postgresql-ip4r_$(OPENRESTY_POSTGRESQL_IP4R_VER)

openresty-postgresql-ip4r-clean:
	cd openresty-postgresql-ip4r && debclean
	-find openresty-postgresql-ip4r -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql-ip4r' -print | xargs rm -rf
	rm -rf openresty-postgresql-ip4r*.deb
	rm -rf openresty-postgresql-ip4r_*.*

.PHONY: openresty-postgresql-ip4r-build
openresty-postgresql-ip4r-build: openresty-postgresql-ip4r-clean openresty-postgresql-ip4r-download
	sudo apt-get -y -q install openresty-postgresql-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql-ip4r_2.4.1.orig.tar.gz --strip-components=1 -C openresty-postgresql-ip4r
	cd openresty-postgresql-ip4r \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
