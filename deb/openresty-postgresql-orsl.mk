## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL_ORSL_VER := 0.02

.PHONY: openresty-postgresql-orsl-download
openresty-postgresql-orsl-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/postgres-orsl-$(OPENRESTY_POSTGRESQL_ORSL_VER).tar.gz ./
	rm -rf openresty-postgresql-orsl_$(OPENRESTY_POSTGRESQL_ORSL_VER)
	mkdir -p openresty-postgresql-orsl_$(OPENRESTY_POSTGRESQL_ORSL_VER)
	tar -xf postgres-orsl-$(OPENRESTY_POSTGRESQL_ORSL_VER).tar.gz --strip-components=1 -C openresty-postgresql-orsl_$(OPENRESTY_POSTGRESQL_ORSL_VER)
	tar -czf openresty-postgresql-orsl_$(OPENRESTY_POSTGRESQL_ORSL_VER).orig.tar.gz openresty-postgresql-orsl_$(OPENRESTY_POSTGRESQL_ORSL_VER)

openresty-postgresql-orsl-clean:
	cd openresty-postgresql-orsl && debclean
	-find openresty-postgresql-orsl -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql-orsl' -print | xargs rm -rf
	rm -rf openresty-postgresql-orsl*.deb
	rm -rf openresty-postgresql-orsl_*.*

.PHONY: openresty-postgresql-orsl-build
openresty-postgresql-orsl-build: openresty-postgresql-orsl-clean openresty-postgresql-orsl-download
	sudo apt-get -y -q install openresty-postgresql-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql-orsl_$(OPENRESTY_POSTGRESQL_ORSL_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql-orsl
	cd openresty-postgresql-orsl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
