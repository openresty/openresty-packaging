## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SAAS_ASAN_VER := $(OR_PLUS_VER)

.PHONY: openresty-saas-asan-download
openresty-saas-asan-download:
	#rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/openresty-plus-$(OPENRESTY_SAAS_ASAN_VER).tar.gz ./
	rm -rf openresty-saas-asan_$(OPENRESTY_SAAS_ASAN_VER)
	mkdir -p openresty-saas-asan_$(OPENRESTY_SAAS_ASAN_VER)
	tar -xf openresty-plus-$(OPENRESTY_SAAS_ASAN_VER).tar.gz --strip-components=1 -C openresty-saas-asan_$(OPENRESTY_SAAS_ASAN_VER)
	tar -czf openresty-saas-asan_$(OPENRESTY_SAAS_ASAN_VER).orig.tar.gz openresty-saas-asan_$(OPENRESTY_SAAS_ASAN_VER)

openresty-saas-asan-clean:
	-cd openresty-saas-asan && debclean
	-find openresty-saas-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-saas-asan' -print | xargs rm -rf
	rm -rf openresty-saas-asan*.deb
	rm -rf openresty-saas-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-saas-asan-build
openresty-saas-asan-build: openresty-saas-asan-clean openresty-saas-asan-download
	sudo apt-get -y -q install ccache gcc make perl ccache gcc make perl openresty-saas-zlib-asan-dev openresty-saas-openssl111-asan-dev openresty-saas-pcre-asan-dev libc-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl ccache gcc make perl openresty-saas-zlib-asan-dev openresty-saas-openssl111-asan-dev openresty-saas-pcre-asan-dev libc-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-saas-asan_$(OPENRESTY_SAAS_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-saas-asan
	cd openresty-saas-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
