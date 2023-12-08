## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SYMGEN_VER := 0.0.8

.PHONY: openresty-symgen-download
openresty-symgen-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/symgen-$(OPENRESTY_SYMGEN_VER).tar.gz ./
	rm -rf openresty-symgen_$(OPENRESTY_SYMGEN_VER)
	mkdir -p openresty-symgen_$(OPENRESTY_SYMGEN_VER)
	tar -xf symgen-$(OPENRESTY_SYMGEN_VER).tar.gz --strip-components=1 -C openresty-symgen_$(OPENRESTY_SYMGEN_VER)
	tar -czf openresty-symgen_$(OPENRESTY_SYMGEN_VER).orig.tar.gz openresty-symgen_$(OPENRESTY_SYMGEN_VER)

openresty-symgen-clean:
	-cd openresty-symgen && debclean
	-find openresty-symgen -maxdepth 1 ! -name 'debian' ! -name 'openresty-symgen' -print | xargs rm -rf
	rm -rf openresty-symgen*.deb
	rm -rf openresty-symgen_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-symgen-build
openresty-symgen-build: openresty-symgen-clean openresty-symgen-download
	sudo apt-get -y -q install ccache gcc make openresty-saas openresty-perl openresty-perl-b-c openresty-perl-cpanel-json-xs openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make openresty-saas openresty-perl openresty-perl-b-c openresty-perl-cpanel-json-xs openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-symgen_$(OPENRESTY_SYMGEN_VER).orig.tar.gz --strip-components=1 -C openresty-symgen
	cd openresty-symgen \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
