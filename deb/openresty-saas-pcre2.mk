## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SAAS_PCRE2_VER = 10.39

.PHONY: openresty-saas-pcre2-download
openresty-saas-pcre2-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/PhilipHazel/pcre2/releases/download/pcre2-$(OPENRESTY_SAAS_PCRE2_VER)/pcre2-$(OPENRESTY_SAAS_PCRE2_VER).tar.gz'
	rm -rf openresty-saas-pcre2_$(OPENRESTY_SAAS_PCRE2_VER)
	mkdir -p openresty-saas-pcre2_$(OPENRESTY_SAAS_PCRE2_VER)
	tar -xf pcre2-$(OPENRESTY_SAAS_PCRE2_VER).tar.gz --strip-components=1 -C openresty-saas-pcre2_$(OPENRESTY_SAAS_PCRE2_VER)
	tar -czf openresty-saas-pcre2_$(OPENRESTY_SAAS_PCRE2_VER).orig.tar.gz openresty-saas-pcre2_$(OPENRESTY_SAAS_PCRE2_VER)

openresty-saas-pcre2-clean:
	-cd openresty-saas-pcre2 && debclean
	-find openresty-saas-pcre2 -maxdepth 1 ! -name 'debian' ! -name 'openresty-saas-pcre2' -print | xargs rm -rf
	rm -rf openresty-saas-pcre2*.deb
	rm -rf openresty-saas-pcre2_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-saas-pcre2-build
openresty-saas-pcre2-build: openresty-saas-pcre2-clean openresty-saas-pcre2-download
	sudo apt-get -y -q install coreutils gcc make ccache sed
	sudo apt-get -y -q install --only-upgrade coreutils gcc libtool make ccache sed
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-saas-pcre2_$(OPENRESTY_SAAS_PCRE2_VER).orig.tar.gz --strip-components=1 -C openresty-saas-pcre2
	cd openresty-saas-pcre2 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
