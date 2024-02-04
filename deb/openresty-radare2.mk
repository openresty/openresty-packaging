## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_RADARE2_VER := 5.0.3.2

.PHONY: openresty-radare2-download
openresty-radare2-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/radare2-plus-$(OPENRESTY_RADARE2_VER).tar.gz ./
	rm -rf openresty-radare2_$(OPENRESTY_RADARE2_VER)
	mkdir -p openresty-radare2_$(OPENRESTY_RADARE2_VER)
	tar -xf radare2-plus-$(OPENRESTY_RADARE2_VER).tar.gz --strip-components=1 -C openresty-radare2_$(OPENRESTY_RADARE2_VER)
	tar -czf openresty-radare2_$(OPENRESTY_RADARE2_VER).orig.tar.gz openresty-radare2_$(OPENRESTY_RADARE2_VER)

openresty-radare2-clean:
	-cd openresty-radare2 && debclean
	-find openresty-radare2 -maxdepth 1 ! -name 'debian' ! -name 'openresty-radare2' -print | xargs rm -rf
	rm -rf openresty-radare2*.deb
	rm -rf openresty-radare2_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-radare2-build
openresty-radare2-build: openresty-radare2-clean openresty-radare2-download
	sudo apt-get -y -q install --no-install-recommends openresty-tcmalloc openresty-tcmalloc-dev git
	sudo apt-get -y -q install --only-upgrade openresty-tcmalloc openresty-tcmalloc-dev git
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-radare2_$(OPENRESTY_RADARE2_VER).orig.tar.gz --strip-components=1 -C openresty-radare2
	cd openresty-radare2 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
