## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LJSB_VER := 1.0.0

.PHONY: openresty-ljsb-download
openresty-ljsb-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/ljsb-$(OPENRESTY_LJSB_VER).tar.gz ./
	rm -rf openresty-ljsb_$(OPENRESTY_LJSB_VER)
	mkdir -p openresty-ljsb_$(OPENRESTY_LJSB_VER)
	tar -xf ljsb-$(OPENRESTY_LJSB_VER).tar.gz --strip-components=1 -C openresty-ljsb_$(OPENRESTY_LJSB_VER)
	tar -czf openresty-ljsb_$(OPENRESTY_LJSB_VER).orig.tar.gz openresty-ljsb_$(OPENRESTY_LJSB_VER)

openresty-ljsb-clean:
	-cd openresty-ljsb && debclean
	-find openresty-ljsb -maxdepth 1 ! -name 'debian' ! -name 'openresty-ljsb' -print | xargs rm -rf
	rm -rf openresty-ljsb*.deb
	rm -rf openresty-ljsb_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-ljsb-build
openresty-ljsb-build: openresty-ljsb-clean openresty-ljsb-download
	sudo apt-get -y -q install ccache cmake gcc make
	sudo apt-get -y -q install --only-upgrade ccache cmake gcc make
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-ljsb_$(OPENRESTY_LJSB_VER).orig.tar.gz --strip-components=1 -C openresty-ljsb
	cd openresty-ljsb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
