## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL_VER := 9.6.20

.PHONY: openresty-postgresql-download
openresty-postgresql-download:
	wget -nH --cut-dirs=100 --mirror 'https://ftp.postgresql.org/pub/source/v$(OPENRESTY_POSTGRESQL_VER)/postgresql-$(OPENRESTY_POSTGRESQL_VER).tar.gz'
	rm -rf openresty-postgresql_$(OPENRESTY_POSTGRESQL_VER)
	mkdir -p openresty-postgresql_$(OPENRESTY_POSTGRESQL_VER)
	tar -xf postgresql-$(OPENRESTY_POSTGRESQL_VER).tar.gz --strip-components=1 -C openresty-postgresql_$(OPENRESTY_POSTGRESQL_VER)
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" ../rpm/SOURCES/openresty-postgresql.init openresty-postgresql_$(OPENRESTY_POSTGRESQL_VER)/
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" ../rpm/SOURCES/openresty-postgresql.service openresty-postgresql_$(OPENRESTY_POSTGRESQL_VER)/
	tar -I 'gzip -1' -cf openresty-postgresql_$(OPENRESTY_POSTGRESQL_VER).orig.tar.gz openresty-postgresql_$(OPENRESTY_POSTGRESQL_VER)

openresty-postgresql-clean:
	-cd openresty-postgresql && debclean
	-find openresty-postgresql -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql' -print | xargs rm -rf
	rm -rf openresty-postgresql*.deb
	rm -rf openresty-postgresql_*.*

.PHONY: openresty-postgresql-build
openresty-postgresql-build: openresty-postgresql-clean openresty-postgresql-download
	sudo apt-get -y -q install ccache libxml2-dev libxslt-dev libossp-uuid-dev libreadline-dev openresty-plus-openssl111-dev
	sudo apt-get -y -q install --only-upgrade ccache libxml2-dev libxslt-dev libossp-uuid-dev libreadline-dev openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql_$(OPENRESTY_POSTGRESQL_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql
	cd openresty-postgresql \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
