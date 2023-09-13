## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_DW2C_VER := 1.5

DEP_OR_PERL_CPANEL_JSON_XS_VER = 4.28-1~$(DISTRO)1

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
	sudo apt-get -y -q install ccache gcc make openresty-perl openresty-perl-b-c openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make openresty-perl openresty-perl-b-c openresty-perl-dev
	# NB: use fixed version number
	sudo apt-get -y -q install openresty-perl-cpanel-json-xs=$(DEP_OR_PERL_CPANEL_JSON_XS_VER)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-dw2c_$(OPENRESTY_DW2C_VER).orig.tar.gz --strip-components=1 -C openresty-dw2c
	cd openresty-dw2c \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage \
			--define perl_cpaneljsonxs_ver=$(DEP_OR_PERL_CPANEL_JSON_XS_VER) \
			debian/control.tt2 > debian/control \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
