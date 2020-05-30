## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PYTHON3_SETUPTOOLS_VER := 39.2.0

.PHONY: openresty-python3-setuptools-download
openresty-python3-setuptools-download:
	wget -nH --cut-dirs=100 --mirror 'https://files.pythonhosted.org/packages/source/s/setuptools/setuptools-$(OPENRESTY_PYTHON3_SETUPTOOLS_VER).zip'
	rm -rf openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)
	mkdir -p openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)
	mkdir -p openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)_tmp
	unzip setuptools-39.2.0.zip -d openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)_tmp
	cp -rf openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)_tmp/setuptools-39.2.0/* openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)
	rm -rf openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)_tmp
	tar -czf openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER).orig.tar.gz openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)

openresty-python3-setuptools-clean:
	cd openresty-python3-setuptools && debclean
	-find openresty-python3-setuptools -maxdepth 1 ! -name 'debian' ! -name 'openresty-python3-setuptools' -print | xargs rm -rf
	rm -rf openresty-python3-setuptools*.deb
	rm -rf openresty-python3-setuptools_*.*

.PHONY: openresty-python3-setuptools-build
openresty-python3-setuptools-build: openresty-python3-setuptools-clean openresty-python3-setuptools-download
	sudo apt-get -y -q install gcc openresty-python3-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-python3-setuptools_39.2.0.orig.tar.gz --strip-components=1 -C openresty-python3-setuptools
	cd openresty-python3-setuptools \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
