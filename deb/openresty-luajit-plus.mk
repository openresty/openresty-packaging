## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LUAJIT_PLUS_VER := 20231123

.PHONY: openresty-luajit-plus-download
openresty-luajit-plus-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/luajit2-plus-$(OPENRESTY_LUAJIT_PLUS_VER).tar.gz ./
	rm -rf openresty-luajit-plus_$(OPENRESTY_LUAJIT_PLUS_VER)
	mkdir -p openresty-luajit-plus_$(OPENRESTY_LUAJIT_PLUS_VER)
	tar -xf luajit2-plus-$(OPENRESTY_LUAJIT_PLUS_VER).tar.gz --strip-components=1 -C openresty-luajit-plus_$(OPENRESTY_LUAJIT_PLUS_VER)
	tar -czf openresty-luajit-plus_$(OPENRESTY_LUAJIT_PLUS_VER).orig.tar.gz openresty-luajit-plus_$(OPENRESTY_LUAJIT_PLUS_VER)

openresty-luajit-plus-clean:
	-cd openresty-luajit-plus && debclean
	-find openresty-luajit-plus -maxdepth 1 ! -name 'debian' ! -name 'openresty-luajit-plus' -print | xargs rm -rf
	rm -rf openresty-luajit-plus*.deb
	rm -rf openresty-luajit-plus_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-luajit-plus-build
openresty-luajit-plus-build: openresty-luajit-plus-clean openresty-luajit-plus-download
	sudo apt-get -y -q install gcc
	sudo apt-get -y -q install --only-upgrade gcc
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-luajit-plus_$(OPENRESTY_LUAJIT_PLUS_VER).orig.tar.gz --strip-components=1 -C openresty-luajit-plus
	cd openresty-luajit-plus \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
