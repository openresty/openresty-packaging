## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PYTHON3_VER := 3.7.14

.PHONY: openresty-python3-download
openresty-python3-download:
	wget -nH --cut-dirs=100 --mirror 'https://www.python.org/ftp/python/$(OPENRESTY_PYTHON3_VER)/Python-$(OPENRESTY_PYTHON3_VER).tar.xz'
	rm -rf openresty-python3_$(OPENRESTY_PYTHON3_VER)
	mkdir -p openresty-python3_$(OPENRESTY_PYTHON3_VER)
	tar -xf Python-$(OPENRESTY_PYTHON3_VER).tar.xz --strip-components=1 -C openresty-python3_$(OPENRESTY_PYTHON3_VER)
	tar czf openresty-python3_$(OPENRESTY_PYTHON3_VER).orig.tar.gz openresty-python3_$(OPENRESTY_PYTHON3_VER)

openresty-python3-clean:
	-cd openresty-python3 && debclean
	-find openresty-python3 -maxdepth 1 ! -name 'debian' ! -name 'openresty-python3' -print | xargs rm -rf
	rm -rf openresty-python3*.deb
	rm -rf openresty-python3_*.*

.PHONY: openresty-python3-build
openresty-python3-build: openresty-python3-clean openresty-python3-download
	sudo apt-get -y -q install libc6-dev ccache gcc make openresty-saas-openssl111-dev libffi-dev libbz2-dev
	sudo apt-get --only-upgrade -y -q install ccache libc6-dev gcc make openresty-saas-openssl111-dev libffi-dev libbz2-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-python3_$(OPENRESTY_PYTHON3_VER).orig.tar.gz --strip-components=1 -C openresty-python3
	cd openresty-python3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
