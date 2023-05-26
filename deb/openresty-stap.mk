## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_STAP_VER := 4.9.0.4

.PHONY: openresty-stap-download
openresty-stap-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/systemtap-plus-$(OPENRESTY_STAP_VER).tar.gz .
	rsync -av systemtap-plus-$(OPENRESTY_STAP_VER).tar.gz openresty-stap_$(OPENRESTY_STAP_VER).orig.tar.gz

openresty-stap-clean:
	-cd openresty-stap && debclean
	-find openresty-stap -maxdepth 1 ! -name 'debian' ! -name 'openresty-stap' -print | xargs rm -rf
	rm -f openresty-stap*.deb
	rm -rf openresty-stap_*.*

.PHONY: openresty-stap-build
openresty-stap-build: openresty-stap-clean openresty-stap-download
	sudo apt-get -y -q install g++ gettext m4 zlib1g-dev liblzma-dev libbz2-dev openresty-elfutils-dev openresty-perl openresty-perl-cpanel-json-xs
	sudo apt-get -y -q --only-upgrade install g++ gettext m4 zlib1g-dev liblzma-dev libbz2-dev openresty-elfutils-dev openresty-perl openresty-perl-cpanel-json-xs
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-stap_$(OPENRESTY_STAP_VER).orig.tar.gz --strip-components=1 -C openresty-stap
	cd openresty-stap \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
