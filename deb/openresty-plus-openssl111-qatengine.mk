## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER := 0.6.4

.PHONY: openresty-plus-openssl111-qatengine-download
openresty-plus-openssl111-qatengine-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/intel/QAT_Engine/archive/v$(OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER).tar.gz'
	rm -rf openresty-plus-openssl111-qatengine_$(OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER)
	mkdir -p openresty-plus-openssl111-qatengine_$(OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER)
	tar -xf v$(OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER).tar.gz --strip-components=1 -C openresty-plus-openssl111-qatengine_$(OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER)
	tar -czf openresty-plus-openssl111-qatengine_$(OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER).orig.tar.gz openresty-plus-openssl111-qatengine_$(OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER)

openresty-plus-openssl111-qatengine-clean:
	-cd openresty-plus-openssl111-qatengine && debclean
	-find openresty-plus-openssl111-qatengine -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-openssl111-qatengine' -print | xargs rm -rf
	rm -rf openresty-plus-openssl111-qatengine*.deb
	rm -rf openresty-plus-openssl111-qatengine_*.*

.PHONY: openresty-plus-openssl111-qatengine-build
openresty-plus-openssl111-qatengine-build: openresty-plus-openssl111-qatengine-clean openresty-plus-openssl111-qatengine-download
	sudo apt-get -y -q install gcc make openresty-plus-openssl111-dev openresty-intel-qat-driver-dev
	sudo apt-get -y -q install --only-upgrade gcc make openresty-plus-openssl111-dev openresty-intel-qat-driver-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-openssl111-qatengine_$(OPENRESTY_PLUS_OPENSSL111_QATENGINE_VER).orig.tar.gz --strip-components=1 -C openresty-plus-openssl111-qatengine
	cd openresty-plus-openssl111-qatengine \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
