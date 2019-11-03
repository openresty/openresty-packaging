## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_BINUTILS_VER := 2.33.1.1

deb_toolchain_pkgs=debhelper devscripts

.PHONY: openresty-binutils-download
openresty-binutils-download:
	rsync -av -e \
		"ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" \
		nuc:~/work/binutils-gdb-plus-$(OPENRESTY_BINUTILS_VER).tar.gz ./
	rm -rf openresty-binutils_$(OPENRESTY_BINUTILS_VER)
	mkdir -p openresty-binutils_$(OPENRESTY_BINUTILS_VER)
	tar -xf binutils-gdb-plus-$(OPENRESTY_BINUTILS_VER).tar.gz --strip-components=1 -C openresty-binutils_$(OPENRESTY_BINUTILS_VER)
	tar -czf openresty-binutils_$(OPENRESTY_BINUTILS_VER).orig.tar.gz openresty-binutils_$(OPENRESTY_BINUTILS_VER)

openresty-binutils-clean:
	cd openresty-binutils && debclean
	-find openresty-binutils -maxdepth 1 ! -name 'debian' ! -name 'openresty-binutils' -print | xargs rm -rf
	rm -rf openresty-binutils*.deb
	rm -rf openresty-binutils_*.*

.PHONY: openresty-binutils-build
openresty-binutils-build: openresty-binutils-clean openresty-binutils-download
	sudo apt-get -y -q install ccache gcc bison flex m4 texinfo g++ gawk sed zlib1g-dev $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-binutils_$(OPENRESTY_BINUTILS_VER).orig.tar.gz --strip-components=1 -C openresty-binutils
	cd openresty-binutils \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
