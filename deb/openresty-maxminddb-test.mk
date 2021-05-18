## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_MAXMINDDB_VER := 1.4.2.4

.PHONY: openresty-maxminddb-test-download
openresty-maxminddb-test-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/libmaxminddb-plus-$(OPENRESTY_MAXMINDDB_VER).tar.gz ./
	rm -rf openresty-maxminddb-test_$(OPENRESTY_MAXMINDDB_VER)
	mkdir -p openresty-maxminddb-test_$(OPENRESTY_MAXMINDDB_VER)
	tar -xf libmaxminddb-plus-$(OPENRESTY_MAXMINDDB_VER).tar.gz --strip-components=1 -C openresty-maxminddb-test_$(OPENRESTY_MAXMINDDB_VER)
	tar -czf openresty-maxminddb-test_$(OPENRESTY_MAXMINDDB_VER).orig.tar.gz openresty-maxminddb-test_$(OPENRESTY_MAXMINDDB_VER)

openresty-maxminddb-test-clean:
	-cd openresty-maxminddb-test && debclean
	-find openresty-maxminddb-test -maxdepth 1 ! -name 'debian' ! -name 'openresty-maxminddb-test' -print | xargs rm -rf
	rm -rf openresty-maxminddb-test*.deb
	rm -rf openresty-maxminddb-test_*.*

.PHONY: openresty-maxminddb-test-build
openresty-maxminddb-test-build: openresty-maxminddb-test-clean openresty-maxminddb-test-download
	sudo apt-get -y -q install ccache
	sudo apt-get -y -q upgrade ccache
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-maxminddb-test_$(OPENRESTY_MAXMINDDB_VER).orig.tar.gz --strip-components=1 -C openresty-maxminddb-test
	cd openresty-maxminddb-test \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
