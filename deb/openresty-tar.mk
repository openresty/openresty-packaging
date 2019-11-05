## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_TAR_VER := 1.32

deb_toolchain_pkgs=debhelper devscripts

.PHONY: openresty-tar-download
openresty-tar-download:
	wget -nH --cut-dirs=100 --mirror 'https://ftp.gnu.org/gnu/tar/tar-$(OPENRESTY_TAR_VER).tar.gz'
	rm -rf openresty-tar_$(OPENRESTY_TAR_VER)
	mkdir -p openresty-tar_$(OPENRESTY_TAR_VER)
	tar -xf tar-$(OPENRESTY_TAR_VER).tar.gz --strip-components=1 -C openresty-tar_$(OPENRESTY_TAR_VER)
	tar -czf openresty-tar_$(OPENRESTY_TAR_VER).orig.tar.gz openresty-tar_$(OPENRESTY_TAR_VER)

openresty-tar-clean:
	cd openresty-tar && debclean
	-find openresty-tar -maxdepth 1 ! -name 'debian' ! -name 'openresty-tar' -print | xargs rm -rf
	rm -rf openresty-tar*.deb
	rm -rf openresty-tar_*.*

.PHONY: openresty-tar-build
openresty-tar-build: openresty-tar-clean openresty-tar-download
	sudo apt-get -y -q install ccache gcc autoconf automake gzip texinfo gettext libacl1-dev gawk $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-tar_$(OPENRESTY_TAR_VER).orig.tar.gz --strip-components=1 -C openresty-tar
	cd openresty-tar \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
