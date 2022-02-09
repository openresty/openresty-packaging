## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBMARIADB_VER := 3.2.5.1

.PHONY: openresty-libmariadb-download
openresty-libmariadb-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/mariadb-connector-c-$(OPENRESTY_LIBMARIADB_VER).tar.gz ./
	rm -rf openresty-libmariadb_$(OPENRESTY_LIBMARIADB_VER)
	mkdir -p openresty-libmariadb_$(OPENRESTY_LIBMARIADB_VER)
	tar -xf mariadb-connector-c-$(OPENRESTY_LIBMARIADB_VER).tar.gz --strip-components=1 -C openresty-libmariadb_$(OPENRESTY_LIBMARIADB_VER)
	tar -czf openresty-libmariadb_$(OPENRESTY_LIBMARIADB_VER).orig.tar.gz openresty-libmariadb_$(OPENRESTY_LIBMARIADB_VER)

openresty-libmariadb-clean:
	-cd openresty-libmariadb && debclean
	-find openresty-libmariadb -maxdepth 1 ! -name 'debian' ! -name 'openresty-libmariadb' -print | xargs rm -rf
	rm -rf openresty-libmariadb*.deb
	rm -rf openresty-libmariadb_*.*

.PHONY: openresty-libmariadb-build
openresty-libmariadb-build: openresty-libmariadb-clean openresty-libmariadb-download
	sudo apt-get -y -q install openresty-plus-openssl111-dev
	sudo apt-get -y -q install --only-upgrade openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libmariadb_$(OPENRESTY_LIBMARIADB_VER).orig.tar.gz --strip-components=1 -C openresty-libmariadb
	cd openresty-libmariadb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
