## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_STAP2_VER := 5.1.0.9

.PHONY: openresty-stap2-download
openresty-stap2-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/systemtap-plus-$(OPENRESTY_STAP2_VER).tar.gz .
	rm -rf openresty-stap2_$(OPENRESTY_STAP2_VER)
	mkdir -p openresty-stap2_$(OPENRESTY_STAP2_VER)
	tar -xf systemtap-plus-$(OPENRESTY_STAP2_VER).tar.gz --strip-components=1 -C openresty-stap2_$(OPENRESTY_STAP2_VER)
	tar -czf openresty-stap2_$(OPENRESTY_STAP2_VER).orig.tar.gz openresty-stap2_$(OPENRESTY_STAP2_VER)

openresty-stap2-clean:
	-cd openresty-stap2 && debclean
	-find openresty-stap2 -maxdepth 1 ! -name 'debian' ! -name 'openresty-stap2' -print | xargs rm -rf
	rm -f openresty-stap2*.deb
	rm -rf openresty-stap2_*.*

.PHONY: openresty-stap2-build
openresty-stap2-build: openresty-stap2-clean openresty-stap2-download
	sudo apt-get -y -q install g++ gettext m4 zlib1g-dev liblzma-dev libbz2-dev openresty-elfutils-dev openresty-perl openresty-perl-cpanel-json-xs
	sudo apt-get -y -q --only-upgrade install g++ gettext m4 zlib1g-dev liblzma-dev libbz2-dev openresty-elfutils-dev openresty-perl openresty-perl-cpanel-json-xs
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-stap2_$(OPENRESTY_STAP2_VER).orig.tar.gz --strip-components=1 -C openresty-stap2
	cd openresty-stap2 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
