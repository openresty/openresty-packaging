## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBDEMANGLE_VER := 11.2.0

.PHONY: openresty-libdemangle-download
openresty-libdemangle-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/gcc-mirror/gcc/archive/refs/tags/releases/gcc-$(OPENRESTY_LIBDEMANGLE_VER).tar.gz'
	rm -rf openresty-libdemangle_$(OPENRESTY_LIBDEMANGLE_VER)
	mkdir -p openresty-libdemangle_$(OPENRESTY_LIBDEMANGLE_VER)
	tar -xf gcc-$(OPENRESTY_LIBDEMANGLE_VER).tar.gz --strip-components=1 -C openresty-libdemangle_$(OPENRESTY_LIBDEMANGLE_VER)
	tar -czf openresty-libdemangle_$(OPENRESTY_LIBDEMANGLE_VER).orig.tar.gz openresty-libdemangle_$(OPENRESTY_LIBDEMANGLE_VER)

openresty-libdemangle-clean:
	-cd openresty-libdemangle && debclean
	-find openresty-libdemangle -maxdepth 1 ! -name 'debian' ! -name 'openresty-libdemangle' -print | xargs rm -rf
	rm -rf openresty-libdemangle*.deb
	rm -rf openresty-libdemangle_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-libdemangle-build
openresty-libdemangle-build: openresty-libdemangle-clean openresty-libdemangle-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libdemangle_$(OPENRESTY_LIBDEMANGLE_VER).orig.tar.gz --strip-components=1 -C openresty-libdemangle
	cd openresty-libdemangle \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
