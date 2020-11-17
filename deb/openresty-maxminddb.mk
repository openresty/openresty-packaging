## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_MAXMINDDB_VER := 1.4.2.4

.PHONY: openresty-maxminddb-download
openresty-maxminddb-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/libmaxminddb-plus-$(OPENRESTY_MAXMINDDB_VER).tar.gz ./
	rm -rf openresty-maxminddb_$(OPENRESTY_MAXMINDDB_VER)
	mkdir -p openresty-maxminddb_$(OPENRESTY_MAXMINDDB_VER)
	tar -xf libmaxminddb-plus-$(OPENRESTY_MAXMINDDB_VER).tar.gz --strip-components=1 -C openresty-maxminddb_$(OPENRESTY_MAXMINDDB_VER)
	tar -czf openresty-maxminddb_$(OPENRESTY_MAXMINDDB_VER).orig.tar.gz openresty-maxminddb_$(OPENRESTY_MAXMINDDB_VER)

openresty-maxminddb-clean:
	-cd openresty-maxminddb && debclean
	-find openresty-maxminddb -maxdepth 1 ! -name 'debian' ! -name 'openresty-maxminddb' -print | xargs rm -rf
	rm -rf openresty-maxminddb*.deb
	rm -rf openresty-maxminddb_*.*

.PHONY: openresty-maxminddb-build
openresty-maxminddb-build: openresty-maxminddb-clean openresty-maxminddb-download
	sudo apt-get -y -q install ccache
	sudo apt-get -y -q upgrade ccache
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-maxminddb_$(OPENRESTY_MAXMINDDB_VER).orig.tar.gz --strip-components=1 -C openresty-maxminddb
	cd openresty-maxminddb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
