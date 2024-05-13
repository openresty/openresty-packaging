## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_MINIFIERS_VER := 0.0.2

.PHONY: openresty-minifiers-download
openresty-minifiers-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/or-minifiers-$(OPENRESTY_MINIFIERS_VER).tar.gz ./
	rm -rf openresty-minifiers_$(OPENRESTY_MINIFIERS_VER)
	mkdir -p openresty-minifiers_$(OPENRESTY_MINIFIERS_VER)
	tar -xf or-minifiers-$(OPENRESTY_MINIFIERS_VER).tar.gz --strip-components=1 -C openresty-minifiers_$(OPENRESTY_MINIFIERS_VER)
	tar -czf openresty-minifiers_$(OPENRESTY_MINIFIERS_VER).orig.tar.gz openresty-minifiers_$(OPENRESTY_MINIFIERS_VER)

openresty-minifiers-clean:
	-cd openresty-minifiers && debclean
	-find openresty-minifiers -maxdepth 1 ! -name 'debian' ! -name 'openresty-minifiers' -print | xargs rm -rf
	rm -rf openresty-minifiers*.deb
	rm -rf openresty-minifiers_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-minifiers-build
openresty-minifiers-build: openresty-minifiers-clean openresty-minifiers-download
	sudo apt-get -y -q install ccache gcc make
	sudo apt-get -y -q install --only-upgrade ccache gcc make
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-minifiers_$(OPENRESTY_MINIFIERS_VER).orig.tar.gz --strip-components=1 -C openresty-minifiers
	cd openresty-minifiers \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
