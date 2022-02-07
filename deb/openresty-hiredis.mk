## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_HIREDIS_VER := 1.0.3.1

.PHONY: openresty-hiredis-download
openresty-hiredis-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/hiredis-$(OPENRESTY_HIREDIS_VER).tar.gz ./
	rm -rf openresty-hiredis_$(OPENRESTY_HIREDIS_VER)
	mkdir -p openresty-hiredis_$(OPENRESTY_HIREDIS_VER)
	tar -xf hiredis-$(OPENRESTY_HIREDIS_VER).tar.gz --strip-components=1 -C openresty-hiredis_$(OPENRESTY_HIREDIS_VER)
	tar -czf openresty-hiredis_$(OPENRESTY_HIREDIS_VER).orig.tar.gz openresty-hiredis_$(OPENRESTY_HIREDIS_VER)

openresty-hiredis-clean:
	-cd openresty-hiredis && debclean
	-find openresty-hiredis -maxdepth 1 ! -name 'debian' ! -name 'openresty-hiredis' -print | xargs rm -rf
	rm -rf openresty-hiredis*.deb
	rm -rf openresty-hiredis_*.*

.PHONY: openresty-hiredis-build
openresty-hiredis-build: openresty-hiredis-clean openresty-hiredis-download
	sudo apt-get -y -q install openresty-plus-openssl111-dev
	sudo apt-get -y -q install --only-upgrade openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-hiredis_$(OPENRESTY_HIREDIS_VER).orig.tar.gz --strip-components=1 -C openresty-hiredis
	cd openresty-hiredis \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
