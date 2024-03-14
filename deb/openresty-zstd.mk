## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ZSTD_VER := 1.5.5

.PHONY: openresty-zstd-download
openresty-zstd-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/facebook/zstd/archive/refs/tags/v$(OPENRESTY_ZSTD_VER).tar.gz'
	rm -rf openresty-zstd_$(OPENRESTY_ZSTD_VER)
	mkdir -p openresty-zstd_$(OPENRESTY_ZSTD_VER)
	tar -xf v$(OPENRESTY_ZSTD_VER).tar.gz --strip-components=1 -C openresty-zstd_$(OPENRESTY_ZSTD_VER)
	tar -czf openresty-zstd_$(OPENRESTY_ZSTD_VER).orig.tar.gz openresty-zstd_$(OPENRESTY_ZSTD_VER)

openresty-zstd-clean:
	-cd openresty-zstd && debclean
	-find openresty-zstd -maxdepth 1 ! -name 'debian' ! -name 'openresty-zstd' -print | xargs rm -rf
	rm -rf openresty-zstd*.deb
	rm -rf openresty-zstd_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-zstd-build
openresty-zstd-build: openresty-zstd-clean openresty-zstd-download
	sudo apt-get -y -q install ccache gcc make
	sudo apt-get -y -q install --only-upgrade ccache gcc make
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-zstd_$(OPENRESTY_ZSTD_VER).orig.tar.gz --strip-components=1 -C openresty-zstd
	cd openresty-zstd \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
