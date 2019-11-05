## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PLZIP_VER := 1.8
OPENRESTY_LZLIB_VER := 1.11

deb_toolchain_pkgs=debhelper devscripts

.PHONY: openresty-plzip-download
openresty-plzip-download:
	wget -nH --cut-dirs=100 --mirror 'http://download.savannah.gnu.org/releases/lzip/plzip/plzip-$(OPENRESTY_PLZIP_VER).tar.gz'
	rm -rf openresty-plzip_$(OPENRESTY_PLZIP_VER)
	mkdir -p openresty-plzip_$(OPENRESTY_PLZIP_VER)
	tar -xf plzip-$(OPENRESTY_PLZIP_VER).tar.gz --strip-components=1 -C openresty-plzip_$(OPENRESTY_PLZIP_VER)
	wget -nH --cut-dirs=100 --mirror 'http://download.savannah.gnu.org/releases/lzip/lzlib/lzlib-$(OPENRESTY_LZLIB_VER).tar.gz'
	mkdir -p openresty-plzip_$(OPENRESTY_PLZIP_VER)/lzlib-$(OPENRESTY_LZLIB_VER)/
	tar -xf lzlib-$(OPENRESTY_LZLIB_VER).tar.gz --strip-components=1 -C openresty-plzip_$(OPENRESTY_PLZIP_VER)/lzlib-$(OPENRESTY_LZLIB_VER)/
	tar -czf openresty-plzip_$(OPENRESTY_PLZIP_VER).orig.tar.gz openresty-plzip_$(OPENRESTY_PLZIP_VER)

openresty-plzip-clean:
	cd openresty-plzip && debclean
	-find openresty-plzip -maxdepth 1 ! -name 'debian' ! -name 'openresty-plzip' -print | xargs rm -rf
	rm -rf openresty-plzip*.deb
	rm -rf openresty-plzip_*.*

.PHONY: openresty-plzip-build
openresty-plzip-build: openresty-plzip-clean openresty-plzip-download
	sudo apt-get -y -q install ccache gcc g++ $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plzip_$(OPENRESTY_PLZIP_VER).orig.tar.gz --strip-components=1 -C openresty-plzip
	cd openresty-plzip \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
