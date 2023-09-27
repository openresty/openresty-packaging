## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBINJECTION_ASAN_VER := 3.10.4

.PHONY: openresty-libinjection-asan-download
openresty-libinjection-asan-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/openresty-libinjection-$(OPENRESTY_LIBINJECTION_ASAN_VER).tar.gz ./
	rm -rf openresty-libinjection-asan_$(OPENRESTY_LIBINJECTION_ASAN_VER)
	mkdir -p openresty-libinjection-asan_$(OPENRESTY_LIBINJECTION_ASAN_VER)
	tar -xf openresty-libinjection-$(OPENRESTY_LIBINJECTION_ASAN_VER).tar.gz --strip-components=1 -C openresty-libinjection-asan_$(OPENRESTY_LIBINJECTION_ASAN_VER)
	tar -czf openresty-libinjection-asan_$(OPENRESTY_LIBINJECTION_ASAN_VER).orig.tar.gz openresty-libinjection-asan_$(OPENRESTY_LIBINJECTION_ASAN_VER)

openresty-libinjection-asan-clean:
	-cd openresty-libinjection-asan && debclean
	-find openresty-libinjection-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-libinjection-asan' -print | xargs rm -rf
	rm -rf openresty-libinjection-asan*.deb
	rm -rf openresty-libinjection-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-libinjection-asan-build
openresty-libinjection-asan-build: openresty-libinjection-asan-clean openresty-libinjection-asan-download
	sudo apt-get -y -q install gcc make openresty-plus-core
	sudo apt-get -y -q install --only-upgrade gcc make openresty-plus-core
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libinjection-asan_$(OPENRESTY_LIBINJECTION_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-libinjection-asan
	cd openresty-libinjection-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
