## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PYTHON3_SETUPTOOLS_VER := 75.1.0

.PHONY: openresty-python3-setuptools-download
openresty-python3-setuptools-download:
	wget -nH --cut-dirs=100 --mirror 'https://files.pythonhosted.org/packages/27/b8/f21073fde99492b33ca357876430822e4800cdf522011f18041351dfa74b/setuptools-$(OPENRESTY_PYTHON3_SETUPTOOLS_VER).tar.gz'
	rm -rf openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)
	mkdir -p openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)
	tar -xf setuptools-$(OPENRESTY_PYTHON3_SETUPTOOLS_VER).tar.gz --strip-components=1 -C openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)
	tar -czf openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER).orig.tar.gz openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER)

openresty-python3-setuptools-clean:
	cd openresty-python3-setuptools && debclean
	-find openresty-python3-setuptools -maxdepth 1 ! -name 'debian' ! -name 'openresty-python3-setuptools' -print | xargs rm -rf
	rm -rf openresty-python3-setuptools*.deb
	rm -rf openresty-python3-setuptools_*.*

.PHONY: openresty-python3-setuptools-build
openresty-python3-setuptools-build: openresty-python3-setuptools-clean openresty-python3-setuptools-download
	sudo apt-get -y -q install gcc openresty-python3-dev automake
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-python3-setuptools_$(OPENRESTY_PYTHON3_SETUPTOOLS_VER).orig.tar.gz --strip-components=1 -C openresty-python3-setuptools
	cd openresty-python3-setuptools \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
