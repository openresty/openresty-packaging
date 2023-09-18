## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SAAS_PCRE_ASAN_VER := $(PCRE_VER)

.PHONY: openresty-saas-pcre-asan-download
openresty-saas-pcre-asan-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://sourceforge.net/projects/pcre/files/pcre/$(OPENRESTY_SAAS_PCRE_ASAN_VER)/pcre-$(OPENRESTY_SAAS_PCRE_ASAN_VER).tar.bz2'
	rm -rf openresty-saas-pcre-asan_$(OPENRESTY_SAAS_PCRE_ASAN_VER)
	mkdir -p openresty-saas-pcre-asan_$(OPENRESTY_SAAS_PCRE_ASAN_VER)
	tar -xf pcre-$(OPENRESTY_SAAS_PCRE_ASAN_VER).tar.bz2 --strip-components=1 -C openresty-saas-pcre-asan_$(OPENRESTY_SAAS_PCRE_ASAN_VER)
	tar -czf openresty-saas-pcre-asan_$(OPENRESTY_SAAS_PCRE_ASAN_VER).orig.tar.gz openresty-saas-pcre-asan_$(OPENRESTY_SAAS_PCRE_ASAN_VER)

openresty-saas-pcre-asan-clean:
	-cd openresty-saas-pcre-asan && debclean
	-find openresty-saas-pcre-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-saas-pcre-asan' -print | xargs rm -rf
	rm -rf openresty-saas-pcre-asan*.deb
	rm -rf openresty-saas-pcre-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-saas-pcre-asan-build
openresty-saas-pcre-asan-build: openresty-saas-pcre-asan-clean openresty-saas-pcre-asan-download
	sudo apt-get -y -q install ccache libtool
	sudo apt-get -y -q install --only-upgrade ccache libtool
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-saas-pcre-asan_$(OPENRESTY_SAAS_PCRE_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-saas-pcre-asan
	cd openresty-saas-pcre-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
