## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_DW2C_VER := 0.2

.PHONY: openresty-dw2c-download
openresty-dw2c-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/dw2c-$(OPENRESTY_DW2C_VER).tar.gz ./
	rm -rf openresty-dw2c_$(OPENRESTY_DW2C_VER)
	mkdir -p openresty-dw2c_$(OPENRESTY_DW2C_VER)
	tar -xf dw2c-$(OPENRESTY_DW2C_VER).tar.gz --strip-components=1 -C openresty-dw2c_$(OPENRESTY_DW2C_VER)
	tar -czf openresty-dw2c_$(OPENRESTY_DW2C_VER).orig.tar.gz openresty-dw2c_$(OPENRESTY_DW2C_VER)

openresty-dw2c-clean:
	-cd openresty-dw2c && debclean
	-find openresty-dw2c -maxdepth 1 ! -name 'debian' ! -name 'openresty-dw2c' -print | xargs rm -rf
	rm -rf openresty-dw2c*.deb
	rm -rf openresty-dw2c_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-dw2c-build
openresty-dw2c-build: openresty-dw2c-clean openresty-dw2c-download
	sudo apt-get -y -q install ccache gcc make openresty-perl openresty-perl-b-c openresty-perl-cpanel-json-xs openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make openresty-perl openresty-perl-b-c openresty-perl-cpanel-json-xs openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-dw2c_$(OPENRESTY_DW2C_VER).orig.tar.gz --strip-components=1 -C openresty-dw2c
	cd openresty-dw2c \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
