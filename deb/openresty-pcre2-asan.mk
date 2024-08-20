## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SAAS_PCRE2_VER = 10.44

.PHONY: openresty-pcre2-asan-download
openresty-pcre2-asan-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/PCRE2Project/pcre2/releases/download/pcre2-$(OPENRESTY_SAAS_PCRE2_VER)/pcre2-$(OPENRESTY_SAAS_PCRE2_VER).tar.gz'
	rm -rf openresty-pcre2_$(OPENRESTY_SAAS_PCRE2_VER)
	mkdir -p openresty-pcre2-asan_$(OPENRESTY_SAAS_PCRE2_VER)
	tar -xf pcre2-$(OPENRESTY_SAAS_PCRE2_VER).tar.gz --strip-components=1 -C openresty-pcre2-asan_$(OPENRESTY_SAAS_PCRE2_VER)
	tar -czf openresty-pcre2-asan_$(OPENRESTY_SAAS_PCRE2_VER).orig.tar.gz openresty-pcre2-asan_$(OPENRESTY_SAAS_PCRE2_VER)

openresty-pcre2-asan-clean:
	-cd openresty-pcre2-asan && debclean
	-find openresty-pcre2-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-pcre2-asan' -print | xargs rm -rf
	rm -rf openresty-pcre2-asan*.deb
	rm -rf openresty-pcre2-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-pcre2-asan-build
openresty-pcre2-asan-build: openresty-pcre2-asan-clean openresty-pcre2-asan-download
	sudo apt-get -y -q install coreutils gcc make ccache sed
	sudo apt-get -y -q install --only-upgrade coreutils gcc libtool make ccache sed
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-pcre2-asan_$(OPENRESTY_SAAS_PCRE2_VER).orig.tar.gz --strip-components=1 -C openresty-pcre2-asan
	cd openresty-pcre2-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
