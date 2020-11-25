## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_MAXMINDDB_DEBUG_VER := 1.4.2.4

.PHONY: openresty-maxminddb-debug-download
openresty-maxminddb-debug-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/libmaxminddb-plus-$(OPENRESTY_MAXMINDDB_DEBUG_VER).tar.gz ./
	rm -rf openresty-maxminddb-debug_$(OPENRESTY_MAXMINDDB_DEBUG_VER)
	mkdir -p openresty-maxminddb-debug_$(OPENRESTY_MAXMINDDB_DEBUG_VER)
	tar -xf libmaxminddb-plus-$(OPENRESTY_MAXMINDDB_DEBUG_VER).tar.gz --strip-components=1 -C openresty-maxminddb-debug_$(OPENRESTY_MAXMINDDB_DEBUG_VER)
	tar -czf openresty-maxminddb-debug_$(OPENRESTY_MAXMINDDB_DEBUG_VER).orig.tar.gz openresty-maxminddb-debug_$(OPENRESTY_MAXMINDDB_DEBUG_VER)

openresty-maxminddb-debug-clean:
	-cd openresty-maxminddb-debug && debclean
	-find openresty-maxminddb-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-maxminddb-debug' -print | xargs rm -rf
	rm -rf openresty-maxminddb-debug*.deb
	rm -rf openresty-maxminddb-debug_*.*

.PHONY: openresty-maxminddb-debug-build
openresty-maxminddb-debug-build: openresty-maxminddb-debug-clean openresty-maxminddb-debug-download
	sudo apt-get -y -q install ccache
	sudo apt-get -y -q upgrade ccache
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-maxminddb-debug_$(OPENRESTY_MAXMINDDB_DEBUG_VER).orig.tar.gz --strip-components=1 -C openresty-maxminddb-debug
	cd openresty-maxminddb-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
