## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ABSL_VER := 20240116.1

.PHONY: openresty-absl-download
openresty-absl-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://github.com/abseil/abseil-cpp/archive/refs/tags/$(OPENRESTY_ABSL_VER).tar.gz'
	rm -rf openresty-absl_$(OPENRESTY_ABSL_VER)
	mkdir -p openresty-absl_$(OPENRESTY_ABSL_VER)
	tar -xf $(OPENRESTY_ABSL_VER).tar.gz --strip-components=1 -C openresty-absl_$(OPENRESTY_ABSL_VER)
	tar -czf openresty-absl_$(OPENRESTY_ABSL_VER).orig.tar.gz openresty-absl_$(OPENRESTY_ABSL_VER)

openresty-absl-clean:
	-cd openresty-absl && debclean
	-find openresty-absl -maxdepth 1 ! -name 'debian' ! -name 'openresty-absl' -print | xargs rm -rf
	rm -rf openresty-absl*.deb
	rm -rf openresty-absl_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-absl-build
openresty-absl-build: openresty-absl-clean openresty-absl-download
	sudo apt-get -y -q install ccache gcc g++ make cmake
	sudo apt-get -y -q install --only-upgrade ccache gcc g++ make cmake
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-absl_$(OPENRESTY_ABSL_VER).orig.tar.gz --strip-components=1 -C openresty-absl
	cd openresty-absl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
