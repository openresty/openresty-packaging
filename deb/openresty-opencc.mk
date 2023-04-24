## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_OPENCC_VER := 1.1.6

.PHONY: openresty-opencc-download
openresty-opencc-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/BYVoid/OpenCC/archive/refs/tags/ver.$(OPENRESTY_OPENCC_VER).tar.gz'
	rm -rf openresty-opencc_$(OPENRESTY_OPENCC_VER)
	mkdir -p openresty-opencc_$(OPENRESTY_OPENCC_VER)
	tar -xf ver.$(OPENRESTY_OPENCC_VER).tar.gz --strip-components=1 -C openresty-opencc_$(OPENRESTY_OPENCC_VER)
	tar -czf openresty-opencc_$(OPENRESTY_OPENCC_VER).orig.tar.gz openresty-opencc_$(OPENRESTY_OPENCC_VER)

openresty-opencc-clean:
	-cd openresty-opencc && debclean
	-find openresty-opencc -maxdepth 1 ! -name 'debian' ! -name 'openresty-opencc' -print | xargs rm -rf
	rm -rf openresty-opencc*.deb
	rm -rf openresty-opencc_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-opencc-build
openresty-opencc-build: openresty-opencc-clean openresty-opencc-download
	sudo apt-get -y -q install gettext cmake
	sudo apt-get -y -q install --only-upgrade gettext cmake
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-opencc_$(OPENRESTY_OPENCC_VER).orig.tar.gz --strip-components=1 -C openresty-opencc
	cd openresty-opencc \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
