## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_COREUTILS_VER := 9.0

.PHONY: openresty-coreutils-download
openresty-coreutils-download:
	wget -nH --cut-dirs=100 --mirror 'http://ftp.gnu.org/gnu/coreutils/coreutils-$(OPENRESTY_COREUTILS_VER).tar.xz'
	rm -rf openresty-coreutils_$(OPENRESTY_COREUTILS_VER)
	mkdir -p openresty-coreutils_$(OPENRESTY_COREUTILS_VER)
	tar -xf coreutils-$(OPENRESTY_COREUTILS_VER).tar.xz --strip-components=1 -C openresty-coreutils_$(OPENRESTY_COREUTILS_VER)
	tar -I 'gzip -1' -cf openresty-coreutils_$(OPENRESTY_COREUTILS_VER).orig.tar.gz openresty-coreutils_$(OPENRESTY_COREUTILS_VER)

openresty-coreutils-clean:
	-cd openresty-coreutils && debclean
	-find openresty-coreutils -maxdepth 1 ! -name 'debian' ! -name 'openresty-coreutils' -print | xargs rm -rf
	rm -rf openresty-coreutils*.deb
	rm -rf openresty-coreutils_*.*

.PHONY: openresty-coreutils-build
openresty-coreutils-build: openresty-coreutils-clean openresty-coreutils-download
	sudo apt-get -y -q install ccache gcc make
	sudo apt-get --only-upgrade -y -q install ccache gcc make
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-coreutils_$(OPENRESTY_COREUTILS_VER).orig.tar.gz --strip-components=1 -C openresty-coreutils
	cd openresty-coreutils \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
