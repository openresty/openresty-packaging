## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PROCSNAP_VER := 3.19.0.4

.PHONY: openresty-procsnap-download
openresty-procsnap-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/criu-plus-$(OPENRESTY_PROCSNAP_VER).tar.gz ./
	rm -rf openresty-procsnap_$(OPENRESTY_PROCSNAP_VER)
	mkdir -p openresty-procsnap_$(OPENRESTY_PROCSNAP_VER)
	tar -xf criu-plus-$(OPENRESTY_PROCSNAP_VER).tar.gz --strip-components=1 -C openresty-procsnap_$(OPENRESTY_PROCSNAP_VER)
	tar -czf openresty-procsnap_$(OPENRESTY_PROCSNAP_VER).orig.tar.gz openresty-procsnap_$(OPENRESTY_PROCSNAP_VER)

openresty-procsnap-clean:
	-cd openresty-procsnap && debclean
	-find openresty-procsnap -maxdepth 1 ! -name 'debian' ! -name 'openresty-procsnap' -print | xargs rm -rf
	rm -rf openresty-procsnap*.deb
	rm -rf openresty-procsnap_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-procsnap-build
openresty-procsnap-build: openresty-procsnap-clean openresty-procsnap-download
	sudo apt-get -y -q install ccache cmake gcc make
	sudo apt-get -y -q install --only-upgrade ccache cmake gcc make
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-procsnap_$(OPENRESTY_PROCSNAP_VER).orig.tar.gz --strip-components=1 -C openresty-procsnap
	cd openresty-procsnap \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
