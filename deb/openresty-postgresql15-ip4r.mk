## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL15_IP4R_VER := 2.4.2

.PHONY: openresty-postgresql15-ip4r-download
openresty-postgresql15-ip4r-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/RhodiumToad/ip4r/archive/$(OPENRESTY_POSTGRESQL15_IP4R_VER).tar.gz'
	rm -rf openresty-postgresql15-ip4r_$(OPENRESTY_POSTGRESQL15_IP4R_VER)
	mkdir -p openresty-postgresql15-ip4r_$(OPENRESTY_POSTGRESQL15_IP4R_VER)
	tar -xf $(OPENRESTY_POSTGRESQL15_IP4R_VER).tar.gz --strip-components=1 -C openresty-postgresql15-ip4r_$(OPENRESTY_POSTGRESQL15_IP4R_VER)
	tar -czf openresty-postgresql15-ip4r_$(OPENRESTY_POSTGRESQL15_IP4R_VER).orig.tar.gz openresty-postgresql15-ip4r_$(OPENRESTY_POSTGRESQL15_IP4R_VER)

openresty-postgresql15-ip4r-clean:
	-cd openresty-postgresql15-ip4r && debclean
	-find openresty-postgresql15-ip4r -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql15-ip4r' -print | xargs rm -rf
	rm -rf openresty-postgresql15-ip4r*.deb
	rm -rf openresty-postgresql15-ip4r_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-postgresql15-ip4r-build
openresty-postgresql15-ip4r-build: openresty-postgresql15-ip4r-clean openresty-postgresql15-ip4r-download
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes -y -q install openresty-postgresql15-dev
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes --only-upgrade -y -q install openresty-postgresql15-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql15-ip4r_$(OPENRESTY_POSTGRESQL15_IP4R_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql15-ip4r
	cd openresty-postgresql15-ip4r \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
