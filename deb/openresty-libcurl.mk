## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBCURL_VER := 7.81.0.2

.PHONY: openresty-libcurl-download
openresty-libcurl-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/curl-plus-$(OPENRESTY_LIBCURL_VER).tar.gz ./
	rm -rf openresty-libcurl_$(OPENRESTY_LIBCURL_VER)
	mkdir -p openresty-libcurl_$(OPENRESTY_LIBCURL_VER)
	tar -xf curl-plus-$(OPENRESTY_LIBCURL_VER).tar.gz --strip-components=1 -C openresty-libcurl_$(OPENRESTY_LIBCURL_VER)
	tar -czf openresty-libcurl_$(OPENRESTY_LIBCURL_VER).orig.tar.gz openresty-libcurl_$(OPENRESTY_LIBCURL_VER)

openresty-libcurl-clean:
	-find openresty-libcurl -maxdepth 1 ! -name 'debian' ! -name 'openresty-libcurl' -print | xargs rm -rf
	-cd openresty-libcurl && debclean
	rm -rf openresty-libcurl*.deb
	rm -rf openresty-libcurl_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-libcurl-build
openresty-libcurl-build: openresty-libcurl-clean openresty-libcurl-download
	sudo apt-get -y -q install automake coreutils gcc libtool make openresty-openssl111-dev openresty-zlib-dev pkg-config sed
	sudo apt-get -y -q install --only-upgrade automake coreutils gcc libtool make openresty-openssl111-dev openresty-zlib-dev pkg-config sed
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libcurl_$(OPENRESTY_LIBCURL_VER).orig.tar.gz --strip-components=1 -C openresty-libcurl
	cd openresty-libcurl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
