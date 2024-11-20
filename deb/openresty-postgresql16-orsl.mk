## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL16_ORSL_VER := 0.02

.PHONY: openresty-postgresql16-orsl-download
openresty-postgresql16-orsl-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/postgres-orsl-$(OPENRESTY_POSTGRESQL16_ORSL_VER).tar.gz ./
	rm -rf openresty-postgresql16-orsl_$(OPENRESTY_POSTGRESQL16_ORSL_VER)
	mkdir -p openresty-postgresql16-orsl_$(OPENRESTY_POSTGRESQL16_ORSL_VER)
	tar -xf postgres-orsl-$(OPENRESTY_POSTGRESQL16_ORSL_VER).tar.gz --strip-components=1 -C openresty-postgresql16-orsl_$(OPENRESTY_POSTGRESQL16_ORSL_VER)
	tar -czf openresty-postgresql16-orsl_$(OPENRESTY_POSTGRESQL16_ORSL_VER).orig.tar.gz openresty-postgresql16-orsl_$(OPENRESTY_POSTGRESQL16_ORSL_VER)

openresty-postgresql16-orsl-clean:
	-cd openresty-postgresql16-orsl && debclean
	-find openresty-postgresql16-orsl -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql16-orsl' -print | xargs rm -rf
	rm -rf openresty-postgresql16-orsl*.deb
	rm -rf openresty-postgresql16-orsl_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-postgresql16-orsl-build
openresty-postgresql16-orsl-build: openresty-postgresql16-orsl-clean openresty-postgresql16-orsl-download
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes -y -q install openresty-postgresql16-dev
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes --only-upgrade -y -q install openresty-postgresql16-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql16-orsl_$(OPENRESTY_POSTGRESQL16_ORSL_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql16-orsl
	cd openresty-postgresql16-orsl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
