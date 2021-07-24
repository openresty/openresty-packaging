## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_GDB_VER := 10.2

.PHONY: openresty-gdb-download
openresty-gdb-download:
	wget -nH --cut-dirs=100 --mirror 'https://ftp.gnu.org/gnu/gdb/gdb-$(OPENRESTY_GDB_VER).tar.xz'
	rm -rf openresty-gdb_$(OPENRESTY_GDB_VER)
	mkdir -p openresty-gdb_$(OPENRESTY_GDB_VER)
	tar -xf gdb-$(OPENRESTY_GDB_VER).tar.xz --strip-components=1 -C openresty-gdb_$(OPENRESTY_GDB_VER)
	tar czf openresty-gdb_$(OPENRESTY_GDB_VER).orig.tar.gz openresty-gdb_$(OPENRESTY_GDB_VER)

openresty-gdb-clean:
	sudo apt-get -y -qq install libc6-dev make gcc g++ texinfo libmpfr-dev openresty-python3-dev liblzma-dev ncurses-dev
	sudo apt-get -y -qq --only-upgrade install libc6-dev make gcc g++ texinfo libmpfr-dev openresty-python3-dev liblzma-dev ncurses-dev
	rm -rf openresty-gdb/debian/.debhelper/
	-cd openresty-gdb && debclean
	-find openresty-gdb -maxdepth 1 ! -name 'debian' ! -name 'openresty-gdb' -print | xargs rm -rf
	rm -rf openresty-gdb*.deb
	rm -rf openresty-gdb_*.*

.PHONY: openresty-gdb-build
openresty-gdb-build: openresty-gdb-clean openresty-gdb-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-gdb_$(OPENRESTY_GDB_VER).orig.tar.gz --strip-components=1 -C openresty-gdb
	cd openresty-gdb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
