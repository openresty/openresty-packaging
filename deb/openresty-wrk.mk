## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_WRK_VER := 4.0.2.1

.PHONY: openresty-wrk-download
openresty-wrk-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/wrk-$(OPENRESTY_WRK_VER).tar.gz ./
	rm -rf openresty-wrk_$(OPENRESTY_WRK_VER)
	mkdir -p openresty-wrk_$(OPENRESTY_WRK_VER)
	tar -xf wrk-$(OPENRESTY_WRK_VER).tar.gz --strip-components=1 -C openresty-wrk_$(OPENRESTY_WRK_VER)
	tar -czf openresty-wrk_$(OPENRESTY_WRK_VER).orig.tar.gz openresty-wrk_$(OPENRESTY_WRK_VER)

openresty-wrk-clean:
	-cd openresty-wrk && debclean
	-find openresty-wrk -maxdepth 1 ! -name 'debian' ! -name 'openresty-wrk' -print | xargs rm -rf
	rm -rf openresty-wrk*.deb
	rm -rf openresty-wrk_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-wrk-build
openresty-wrk-build: openresty-wrk-clean openresty-wrk-download
	sudo apt-get -y -q install gcc make openresty-plus-core-dev openresty-plus-openssl111-dev
	sudo apt-get -y -q install --only-upgrade gcc make openresty-plus-core-dev openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-wrk_$(OPENRESTY_WRK_VER).orig.tar.gz --strip-components=1 -C openresty-wrk
	cd openresty-wrk \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
