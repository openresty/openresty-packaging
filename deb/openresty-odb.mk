## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ODB_VER := 0.23

.PHONY: openresty-odb-download
openresty-odb-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/odb-$(OPENRESTY_ODB_VER).tar.gz ./
	rm -rf openresty-odb_$(OPENRESTY_ODB_VER)
	mkdir -p openresty-odb_$(OPENRESTY_ODB_VER)
	tar -xf odb-$(OPENRESTY_ODB_VER).tar.gz --strip-components=1 -C openresty-odb_$(OPENRESTY_ODB_VER)
	tar -czf openresty-odb_$(OPENRESTY_ODB_VER).orig.tar.gz openresty-odb_$(OPENRESTY_ODB_VER)

openresty-odb-clean:
	-cd openresty-odb && debclean
	-find openresty-odb -maxdepth 1 ! -name 'debian' ! -name 'openresty-odb' -print | xargs rm -rf
	rm -rf openresty-odb*.deb
	rm -rf openresty-odb_*.*

.PHONY: openresty-odb-build
openresty-odb-build: openresty-odb-clean openresty-odb-download
	sudo apt-get -y -q install ccache g++ openresty-saas-pcre-dev
	sudo apt-get -y -q --only-upgrade install ccache g++ openresty-saas-pcre-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-odb_$(OPENRESTY_ODB_VER).orig.tar.gz --strip-components=1 -C openresty-odb
	cd openresty-odb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
