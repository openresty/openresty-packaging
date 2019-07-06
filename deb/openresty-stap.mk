## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_STAP_VER := 4.2.0.2

.PHONY: openresty-stap-download
openresty-stap-download:
	rsync -av nuc:~/work/systemtap-plus-$(OPENRESTY_STAP_VER).tar.gz .
	rsync -av systemtap-plus-4.2.0.2.tar.gz openresty-stap_$(OPENRESTY_STAP_VER).orig.tar.gz

openresty-stap-clean:
	cd openresty-stap && debclean
	-find openresty-stap -maxdepth 1 ! -name 'debian' ! -name 'openresty-stap' -print | xargs rm -rf
	rm -f openresty-stap*.deb
	rm -f openresty-stap_*.*

.PHONY: openresty-stap-build
openresty-stap-build: openresty-stap-clean openresty-stap-download
	sudo apt-get -y -q install g++ gettext m4 zlib1g-dev liblzma-dev openresty-elfutils-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-stap_4.2.0.2.orig.tar.gz --strip-components=1 -C openresty-stap
	cd openresty-stap \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
