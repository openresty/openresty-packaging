## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PYTHON3_CYTHON_VER := 3.0.11

.PHONY: openresty-python3-cython-download
openresty-python3-cython-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/cython/cython/releases/download/$(OPENRESTY_PYTHON3_CYTHON_VER)-1/cython-$(OPENRESTY_PYTHON3_CYTHON_VER).tar.gz'
	rm -rf openresty-python3-cython_$(OPENRESTY_PYTHON3_CYTHON_VER)
	mkdir -p openresty-python3-cython_$(OPENRESTY_PYTHON3_CYTHON_VER)
	tar -xf cython-$(OPENRESTY_PYTHON3_CYTHON_VER).tar.gz --strip-components=1 -C openresty-python3-cython_$(OPENRESTY_PYTHON3_CYTHON_VER)
	tar -czf openresty-python3-cython_$(OPENRESTY_PYTHON3_CYTHON_VER).orig.tar.gz openresty-python3-cython_$(OPENRESTY_PYTHON3_CYTHON_VER)

openresty-python3-cython-clean:
	cd openresty-python3-cython && debclean
	-find openresty-python3-cython -maxdepth 1 ! -name 'debian' ! -name 'openresty-python3-cython' -print | xargs rm -rf
	rm -rf openresty-python3-cython*.deb
	rm -rf openresty-python3-cython_*.*

.PHONY: openresty-python3-cython-build
openresty-python3-cython-build: openresty-python3-cython-clean openresty-python3-cython-download
	sudo apt-get -y -q install gcc openresty-python3-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-python3-cython_$(OPENRESTY_PYTHON3_CYTHON_VER).orig.tar.gz --strip-components=1 -C openresty-python3-cython
	cd openresty-python3-cython \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
