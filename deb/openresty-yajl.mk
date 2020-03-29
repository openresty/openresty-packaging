## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_YAJL_VER := 2.1.0.3

.PHONY: openresty-yajl-download
openresty-yajl-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/yajl-plus-$(OPENRESTY_YAJL_VER).tar.gz .
	rsync -av yajl-plus-$(OPENRESTY_YAJL_VER).tar.gz openresty-yajl_$(OPENRESTY_YAJL_VER).orig.tar.gz

openresty-yajl-clean:
	cd openresty-yajl && debclean
	-find openresty-yajl -maxdepth 1 ! -name 'debian' ! -name 'openresty-yajl' -print | xargs rm -rf
	rm -f openresty-yajl*.deb
	rm -f openresty-yajl_*.*

.PHONY: openresty-yajl-build
openresty-yajl-build: openresty-yajl-clean openresty-yajl-download
	sudo apt-get -y -q install cmake
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-yajl_$(OPENRESTY_YAJL_VER).orig.tar.gz --strip-components=1 -C openresty-yajl
	cd openresty-yajl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
