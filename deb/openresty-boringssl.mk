## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_BORINGSSL_VER := 20221129

.PHONY: openresty-boringssl-download
openresty-boringssl-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/boringssl-plus-$(OPENRESTY_BORINGSSL_VER).tar.gz ./
	rm -rf openresty-boringssl_$(OPENRESTY_BORINGSSL_VER)
	mkdir -p openresty-boringssl_$(OPENRESTY_BORINGSSL_VER)
	tar -xf boringssl-plus-$(OPENRESTY_BORINGSSL_VER).tar.gz --strip-components=1 -C openresty-boringssl_$(OPENRESTY_BORINGSSL_VER)
	tar -czf openresty-boringssl_$(OPENRESTY_BORINGSSL_VER).orig.tar.gz openresty-boringssl_$(OPENRESTY_BORINGSSL_VER)

openresty-boringssl-clean:
	-cd openresty-boringssl && debclean
	-find openresty-boringssl -maxdepth 1 ! -name 'debian' ! -name 'openresty-boringssl' -print | xargs rm -rf
	rm -rf openresty-boringssl*.deb
	rm -rf openresty-boringssl_*.*

.PHONY: openresty-boringssl-build
openresty-boringssl-build: openresty-boringssl-clean openresty-boringssl-download
	sudo apt-get -y -q install gcc make g++ openresty-zlib-dev libunwind-dev
	sudo apt-get -y -q install --only-upgrade gcc make g++ openresty-zlib-dev libunwind-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-boringssl_$(OPENRESTY_BORINGSSL_VER).orig.tar.gz --strip-components=1 -C openresty-boringssl
	cd openresty-boringssl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian --preserve-envvar PATH $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
