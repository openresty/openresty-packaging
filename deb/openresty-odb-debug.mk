## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ODB_VER := 0.08

.PHONY: openresty-odb-debug-download
openresty-odb-debug-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/odb-$(OPENRESTY_ODB_VER).tar.gz ./
	rm -rf openresty-odb-debug_$(OPENRESTY_ODB_VER)
	mkdir -p openresty-odb-debug_$(OPENRESTY_ODB_VER)
	tar -xf odb-$(OPENRESTY_ODB_VER).tar.gz --strip-components=1 -C openresty-odb-debug_$(OPENRESTY_ODB_VER)
	tar -czf openresty-odb-debug_$(OPENRESTY_ODB_VER).orig.tar.gz openresty-odb-debug_$(OPENRESTY_ODB_VER)

openresty-odb-debug-clean:
	-cd openresty-odb-debug && debclean
	-find openresty-odb-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-odb-debug' -print | xargs rm -rf
	rm -rf openresty-odb-debug*.deb
	rm -rf openresty-odb-debug_*.*

.PHONY: openresty-odb-debug-build
openresty-odb-debug-build: openresty-odb-debug-clean openresty-odb-debug-download
	sudo apt-get -y -q install ccache g++ openresty-saas-pcre-dev
	sudo apt-get -y -q --only-upgrade install ccache g++ openresty-saas-pcre-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-odb-debug_$(OPENRESTY_ODB_VER).orig.tar.gz --strip-components=1 -C openresty-odb-debug
	cd openresty-odb-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
