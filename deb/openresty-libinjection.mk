## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBINJECTION_VER := 3.10.2

.PHONY: openresty-libinjection-download
openresty-libinjection-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/openresty-libinjection-$(OPENRESTY_LIBINJECTION_VER).tar.gz ./
	rm -rf openresty-libinjection_$(OPENRESTY_LIBINJECTION_VER)
	mkdir -p openresty-libinjection_$(OPENRESTY_LIBINJECTION_VER)
	tar -xf openresty-libinjection-$(OPENRESTY_LIBINJECTION_VER).tar.gz --strip-components=1 -C openresty-libinjection_$(OPENRESTY_LIBINJECTION_VER)
	tar -czf openresty-libinjection_$(OPENRESTY_LIBINJECTION_VER).orig.tar.gz openresty-libinjection_$(OPENRESTY_LIBINJECTION_VER)

openresty-libinjection-clean:
	-cd openresty-libinjection && debclean
	-find openresty-libinjection -maxdepth 1 ! -name 'debian' ! -name 'openresty-libinjection' -print | xargs rm -rf
	rm -rf openresty-libinjection*.deb
	rm -rf openresty-libinjection_*.*

.PHONY: openresty-libinjection-build
openresty-libinjection-build: openresty-libinjection-clean openresty-libinjection-download
	sudo apt-get -y -q install gcc make openresty-plus-core
	sudo apt-get -y -q install --only-upgrade gcc make openresty-plus-core
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libinjection_$(OPENRESTY_LIBINJECTION_VER).orig.tar.gz --strip-components=1 -C openresty-libinjection
	cd openresty-libinjection \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
