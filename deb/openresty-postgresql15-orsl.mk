## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL15_ORSL_VER := 0.02

.PHONY: openresty-postgresql15-orsl-download
openresty-postgresql15-orsl-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/postgres-orsl-$(OPENRESTY_POSTGRESQL15_ORSL_VER).tar.gz ./
	rm -rf openresty-postgresql15-orsl_$(OPENRESTY_POSTGRESQL15_ORSL_VER)
	mkdir -p openresty-postgresql15-orsl_$(OPENRESTY_POSTGRESQL15_ORSL_VER)
	tar -xf postgres-orsl-$(OPENRESTY_POSTGRESQL15_ORSL_VER).tar.gz --strip-components=1 -C openresty-postgresql15-orsl_$(OPENRESTY_POSTGRESQL15_ORSL_VER)
	tar -czf openresty-postgresql15-orsl_$(OPENRESTY_POSTGRESQL15_ORSL_VER).orig.tar.gz openresty-postgresql15-orsl_$(OPENRESTY_POSTGRESQL15_ORSL_VER)

openresty-postgresql15-orsl-clean:
	-cd openresty-postgresql15-orsl && debclean
	-find openresty-postgresql15-orsl -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql15-orsl' -print | xargs rm -rf
	rm -rf openresty-postgresql15-orsl*.deb
	rm -rf openresty-postgresql15-orsl_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-postgresql15-orsl-build
openresty-postgresql15-orsl-build: openresty-postgresql15-orsl-clean openresty-postgresql15-orsl-download
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes -y -q install openresty-postgresql15-dev
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes --only-upgrade -y -q install openresty-postgresql15-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql15-orsl_$(OPENRESTY_POSTGRESQL15_ORSL_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql15-orsl
	cd openresty-postgresql15-orsl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
