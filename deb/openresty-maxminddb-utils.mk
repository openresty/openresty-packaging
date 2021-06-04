## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_MAXMINDDB_UTILS_VER := 0.0.3

.PHONY: openresty-maxminddb-utils-download
openresty-maxminddb-utils-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/maxminddb-utils-$(OPENRESTY_MAXMINDDB_UTILS_VER).tar.gz ./
	rm -rf openresty-maxminddb-utils_$(OPENRESTY_MAXMINDDB_UTILS_VER)
	mkdir -p openresty-maxminddb-utils_$(OPENRESTY_MAXMINDDB_UTILS_VER)
	tar -xf maxminddb-utils-$(OPENRESTY_MAXMINDDB_UTILS_VER).tar.gz --strip-components=1 -C openresty-maxminddb-utils_$(OPENRESTY_MAXMINDDB_UTILS_VER)
	tar -czf openresty-maxminddb-utils_$(OPENRESTY_MAXMINDDB_UTILS_VER).orig.tar.gz openresty-maxminddb-utils_$(OPENRESTY_MAXMINDDB_UTILS_VER)

openresty-maxminddb-utils-clean:
	-cd openresty-maxminddb-utils && debclean
	-find openresty-maxminddb-utils -maxdepth 1 ! -name 'debian' ! -name 'openresty-maxminddb-utils' -print | xargs rm -rf
	rm -rf openresty-maxminddb-utils*.deb
	rm -rf openresty-maxminddb-utils_*.*

.PHONY: openresty-maxminddb-utils-build
openresty-maxminddb-utils-build: openresty-maxminddb-utils-clean openresty-maxminddb-utils-download
	sudo apt-get -y -q install make
	sudo apt-get -y -q install --only-upgrade make
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-maxminddb-utils_$(OPENRESTY_MAXMINDDB_UTILS_VER).orig.tar.gz --strip-components=1 -C openresty-maxminddb-utils
	cd openresty-maxminddb-utils \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
