## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_INTEL_QAT_DRIVER_VER := 1.7.l.4.11.0

.PHONY: openresty-intel-qat-driver-download
openresty-intel-qat-driver-download:
	wget -nH --cut-dirs=100 --mirror 'https://01.org/sites/default/files/downloads//qat$(OPENRESTY_INTEL_QAT_DRIVER_VER)-00001.tar.gz'
	rm -rf openresty-intel-qat-driver_$(OPENRESTY_INTEL_QAT_DRIVER_VER)
	mkdir -p openresty-intel-qat-driver_$(OPENRESTY_INTEL_QAT_DRIVER_VER)
	tar -xf qat$(OPENRESTY_INTEL_QAT_DRIVER_VER)-00001.tar.gz --strip-components=1 -C openresty-intel-qat-driver_$(OPENRESTY_INTEL_QAT_DRIVER_VER)
	tar -czf openresty-intel-qat-driver_$(OPENRESTY_INTEL_QAT_DRIVER_VER).orig.tar.gz openresty-intel-qat-driver_$(OPENRESTY_INTEL_QAT_DRIVER_VER)

openresty-intel-qat-driver-clean:
	-cd openresty-intel-qat-driver && debclean
	-find openresty-intel-qat-driver -maxdepth 1 ! -name 'debian' ! -name 'openresty-intel-qat-driver' -print | xargs rm -rf
	rm -rf openresty-intel-qat-driver*.deb
	rm -rf openresty-intel-qat-driver_*.*

.PHONY: openresty-intel-qat-driver-build
openresty-intel-qat-driver-build: openresty-intel-qat-driver-clean openresty-intel-qat-driver-download
	sudo apt-get -y -q install gcc make ccache
	sudo apt-get -y -q install --only-upgrade gcc make ccache
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-intel-qat-driver_$(OPENRESTY_INTEL_QAT_DRIVER_VER).orig.tar.gz --strip-components=1 -C openresty-intel-qat-driver
	cd openresty-intel-qat-driver \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
