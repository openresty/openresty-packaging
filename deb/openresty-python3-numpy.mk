## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PYTHON3_NUMPY_VER := 2.1.1

.PHONY: openresty-python3-numpy-download
openresty-python3-numpy-download:
	wget -nH --cut-dirs=100 --mirror https://github.com/numpy/numpy/releases/download/v$(OPENRESTY_PYTHON3_NUMPY_VER)/numpy-$(OPENRESTY_PYTHON3_NUMPY_VER).tar.gz
	rm -rf openresty-python3-numpy_$(OPENRESTY_PYTHON3_NUMPY_VER)
	mkdir -p openresty-python3-numpy_$(OPENRESTY_PYTHON3_NUMPY_VER)
	tar -xf numpy-$(OPENRESTY_PYTHON3_NUMPY_VER).tar.gz --strip-components=1 -C openresty-python3-numpy_$(OPENRESTY_PYTHON3_NUMPY_VER)
	tar -czf openresty-python3-numpy_$(OPENRESTY_PYTHON3_NUMPY_VER).orig.tar.gz openresty-python3-numpy_$(OPENRESTY_PYTHON3_NUMPY_VER)

openresty-python3-numpy-clean:
	cd openresty-python3-numpy && debclean
	-find openresty-python3-numpy -maxdepth 1 ! -name 'debian' ! -name 'openresty-python3-numpy' -print | xargs rm -rf
	rm -rf openresty-python3-numpy*.deb
	rm -rf openresty-python3-numpy_*.*

.PHONY: openresty-python3-numpy-build
openresty-python3-numpy-build: openresty-python3-numpy-clean openresty-python3-numpy-download
	sudo apt-get -y -q install liblapack-dev gfortran gcc openresty-python3-dev libatlas-base-dev openresty-python3-setuptools openresty-python3-cython
	#wget https://github.com/ninja-build/ninja/releases/download/v1.12.1/ninja-linux.zip
	#unzip ninja-linux.zip
	#sudo mv ninja /usr/bin
	#wget https://bootstrap.pypa.io/get-pip.py
	#sudo /usr/local/openresty-python3/bin/python3 get-pip.py
	#rm -f get-pip.py
	#sudo /usr/local/openresty-python3/bin/python3 -m pip install meson
	#sudo /usr/local/openresty-python3/bin/python3 -m pip install spin
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-python3-numpy_$(OPENRESTY_PYTHON3_NUMPY_VER).orig.tar.gz --strip-components=1 -C openresty-python3-numpy
	cd openresty-python3-numpy \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
