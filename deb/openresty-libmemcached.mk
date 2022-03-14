## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBMEMCACHED_VER := 1.2.3

.PHONY: openresty-libmemcached-download
openresty-libmemcached-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/libmemcached-plus-$(OPENRESTY_LIBMEMCACHED_VER).tar.gz ./
	rm -rf openresty-libmemcached_$(OPENRESTY_LIBMEMCACHED_VER)
	mkdir -p openresty-libmemcached_$(OPENRESTY_LIBMEMCACHED_VER)
	tar -xf libmemcached-plus-$(OPENRESTY_LIBMEMCACHED_VER).tar.gz --strip-components=1 -C openresty-libmemcached_$(OPENRESTY_LIBMEMCACHED_VER)
	tar -czf openresty-libmemcached_$(OPENRESTY_LIBMEMCACHED_VER).orig.tar.gz openresty-libmemcached_$(OPENRESTY_LIBMEMCACHED_VER)

openresty-libmemcached-clean:
	-cd openresty-libmemcached && debclean
	-find openresty-libmemcached -maxdepth 1 ! -name 'debian' ! -name 'openresty-libmemcached' -print | xargs rm -rf
	rm -rf openresty-libmemcached*.deb
	rm -rf openresty-libmemcached_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-libmemcached-build
openresty-libmemcached-build: openresty-libmemcached-clean openresty-libmemcached-download
	sudo apt-get -y -q install libtool autoconf automake bison flex openresty-cyrus-sasl-dev openresty-plus-openssl111-dev
	sudo apt-get -y -q install --only-upgrade libtool autoconf automake bison flex openresty-cyrus-sasl-dev openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libmemcached_$(OPENRESTY_LIBMEMCACHED_VER).orig.tar.gz --strip-components=1 -C openresty-libmemcached
	cd openresty-libmemcached \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
