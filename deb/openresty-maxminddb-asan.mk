## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_MAXMINDDB_ASAN_VER := 1.4.2.4

.PHONY: openresty-maxminddb-asan-download
openresty-maxminddb-asan-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/libmaxminddb-plus-$(OPENRESTY_MAXMINDDB_ASAN_VER).tar.gz ./
	rm -rf openresty-maxminddb-asan_$(OPENRESTY_MAXMINDDB_ASAN_VER)
	mkdir -p openresty-maxminddb-asan_$(OPENRESTY_MAXMINDDB_ASAN_VER)
	tar -xf libmaxminddb-plus-$(OPENRESTY_MAXMINDDB_ASAN_VER).tar.gz --strip-components=1 -C openresty-maxminddb-asan_$(OPENRESTY_MAXMINDDB_ASAN_VER)
	tar -czf openresty-maxminddb-asan_$(OPENRESTY_MAXMINDDB_ASAN_VER).orig.tar.gz openresty-maxminddb-asan_$(OPENRESTY_MAXMINDDB_ASAN_VER)

openresty-maxminddb-asan-clean:
	-cd openresty-maxminddb-asan && debclean
	-find openresty-maxminddb-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-maxminddb-asan' -print | xargs rm -rf
	rm -rf openresty-maxminddb-asan*.deb
	rm -rf openresty-maxminddb-asan_*.*

.PHONY: openresty-maxminddb-asan-build
openresty-maxminddb-asan-build: openresty-maxminddb-asan-clean openresty-maxminddb-asan-download
	sudo apt-get -y -q install ccache make gcc
	sudo apt-get -y -q install --only-upgrade ccache make gcc
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-maxminddb-asan_$(OPENRESTY_MAXMINDDB_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-maxminddb-asan
	cd openresty-maxminddb-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
