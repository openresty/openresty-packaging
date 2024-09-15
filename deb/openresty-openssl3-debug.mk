## Author: spec2deb.pl
### Version: 0.01

.PHONY: openresty-openssl3-debug-download
openresty-openssl3-debug-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/openssl/openssl/releases/download/openssl-$(SSL3_VER)/openssl-$(SSL3_VER).tar.gz'
	rm -rf openresty-openssl3-debug_$(SSL3_VER)
	mkdir -p openresty-openssl3-debug_$(SSL3_VER)
	tar -xf openssl-$(SSL3_VER).tar.gz --strip-components=1 -C openresty-openssl3-debug_$(SSL3_VER)
	tar -czf openresty-openssl3-debug_$(SSL3_VER).orig.tar.gz openresty-openssl3-debug_$(SSL3_VER)

openresty-openssl3-debug-clean:
	-cd openresty-openssl3-debug && debclean
	-find openresty-openssl3-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-openssl3-debug' -print | xargs rm -rf
	rm -rf openresty-openssl3-debug*.deb
	rm -rf openresty-openssl3-debug_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-openssl3-debug-build
openresty-openssl3-debug-build: openresty-openssl3-debug-clean openresty-openssl3-debug-download
	sudo apt-get -y -q install gcc make perl openresty-zlib-dev
	sudo apt-get -y -q install --only-upgrade gcc make perl openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl3-debug_$(SSL3_VER).orig.tar.gz --strip-components=1 -C openresty-openssl3-debug
	cd openresty-openssl3-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
