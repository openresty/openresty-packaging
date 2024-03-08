## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_GDB_RUNTIME_VER := 0.0.4

.PHONY: openresty-gdb-runtime-download
openresty-gdb-runtime-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/gdb-runtime-$(OPENRESTY_GDB_RUNTIME_VER).tar.gz ./
	rm -rf openresty-gdb-runtime_$(OPENRESTY_GDB_RUNTIME_VER)
	mkdir -p openresty-gdb-runtime_$(OPENRESTY_GDB_RUNTIME_VER)
	tar -xf gdb-runtime-$(OPENRESTY_GDB_RUNTIME_VER).tar.gz --strip-components=1 -C openresty-gdb-runtime_$(OPENRESTY_GDB_RUNTIME_VER)
	tar -czf openresty-gdb-runtime_$(OPENRESTY_GDB_RUNTIME_VER).orig.tar.gz openresty-gdb-runtime_$(OPENRESTY_GDB_RUNTIME_VER)

openresty-gdb-runtime-clean:
	-cd openresty-gdb-runtime && debclean
	-find openresty-gdb-runtime -maxdepth 1 ! -name 'debian' ! -name 'openresty-gdb-runtime' -print | xargs rm -rf
	rm -rf openresty-gdb-runtime*.deb
	rm -rf openresty-gdb-runtime_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-gdb-runtime-build
openresty-gdb-runtime-build: openresty-gdb-runtime-clean openresty-gdb-runtime-download
	sudo apt-get -y -q install g++ openresty-saas-pcre-dev
	sudo apt-get -y -q install --only-upgrade g++ openresty-saas-pcre-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-gdb-runtime_$(OPENRESTY_GDB_RUNTIME_VER).orig.tar.gz --strip-components=1 -C openresty-gdb-runtime
	cd openresty-gdb-runtime \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
