## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL12_ORSL_VER := 0.02

.PHONY: openresty-postgresql12-orsl-download
openresty-postgresql12-orsl-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/postgres-orsl-$(OPENRESTY_POSTGRESQL12_ORSL_VER).tar.gz ./
	rm -rf openresty-postgresql12-orsl_$(OPENRESTY_POSTGRESQL12_ORSL_VER)
	mkdir -p openresty-postgresql12-orsl_$(OPENRESTY_POSTGRESQL12_ORSL_VER)
	tar -xf postgres-orsl-$(OPENRESTY_POSTGRESQL12_ORSL_VER).tar.gz --strip-components=1 -C openresty-postgresql12-orsl_$(OPENRESTY_POSTGRESQL12_ORSL_VER)
	tar -czf openresty-postgresql12-orsl_$(OPENRESTY_POSTGRESQL12_ORSL_VER).orig.tar.gz openresty-postgresql12-orsl_$(OPENRESTY_POSTGRESQL12_ORSL_VER)

openresty-postgresql12-orsl-clean:
	cd openresty-postgresql12-orsl && debclean
	-find openresty-postgresql12-orsl -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql12-orsl' -print | xargs rm -rf
	rm -rf openresty-postgresql12-orsl*.deb
	rm -rf openresty-postgresql12-orsl_*.*

.PHONY: openresty-postgresql12-orsl-build
openresty-postgresql12-orsl-build: openresty-postgresql12-orsl-clean openresty-postgresql12-orsl-download
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes -y -q install openresty-postgresql12-dev
	sudo apt-get -o Dpkg::Options::="--force-confold" --force-yes --only-upgrade -y -q install openresty-postgresql12-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql12-orsl_$(OPENRESTY_POSTGRESQL12_ORSL_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql12-orsl
	cd openresty-postgresql12-orsl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
