## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_EDGCPFE_VER := 6.6.0.8

.PHONY: openresty-edgcpfe-download
openresty-edgcpfe-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/edgcpfe-plus-$(OPENRESTY_EDGCPFE_VER).tar.gz ./
	rm -rf openresty-edgcpfe_$(OPENRESTY_EDGCPFE_VER)
	mkdir -p openresty-edgcpfe_$(OPENRESTY_EDGCPFE_VER)
	tar -xf edgcpfe-plus-$(OPENRESTY_EDGCPFE_VER).tar.gz --strip-components=1 -C openresty-edgcpfe_$(OPENRESTY_EDGCPFE_VER)
	tar -czf openresty-edgcpfe_$(OPENRESTY_EDGCPFE_VER).orig.tar.gz openresty-edgcpfe_$(OPENRESTY_EDGCPFE_VER)

openresty-edgcpfe-clean:
	-cd openresty-edgcpfe && debclean
	-find openresty-edgcpfe -maxdepth 1 ! -name 'debian' ! -name 'openresty-edgcpfe' -print | xargs rm -rf
	rm -rf openresty-edgcpfe*.deb
	rm -rf openresty-edgcpfe_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-edgcpfe-build
openresty-edgcpfe-build: openresty-edgcpfe-clean openresty-edgcpfe-download
	sudo apt-get -y -q install ccache gcc g++
	sudo apt-get -y -q install --only-upgrade ccache gcc g++
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-edgcpfe_$(OPENRESTY_EDGCPFE_VER).orig.tar.gz --strip-components=1 -C openresty-edgcpfe
	cd openresty-edgcpfe \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
