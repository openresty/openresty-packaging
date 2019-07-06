## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ELFUTILS_VER := 0.176.6

.PHONY: openresty-elfutils-download
openresty-elfutils-download:
	rsync -av nuc:~/work/elfutils-plus-$(OPENRESTY_ELFUTILS_VER).tar.gz .
	rsync -av elfutils-plus-0.176.6.tar.gz openresty-elfutils_$(OPENRESTY_ELFUTILS_VER).orig.tar.gz

openresty-elfutils-clean:
	cd openresty-elfutils && debclean
	find openresty-elfutils -maxdepth 1 ! -name 'debian' ! -name 'openresty-elfutils' -print | xargs rm -rf
	rm -f openresty-elfutils*.deb
	rm -f openresty-elfutils_*.*

.PHONY: openresty-elfutils-build
openresty-elfutils-build: openresty-elfutils-clean openresty-elfutils-download
	sudo apt-get -y -q install gcc libc6 bison flex libbz2-dev m4 gettext zlib1g-dev libbz2-dev liblzma-dev g++ autoconf openresty-yajl-dev gawk sed
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-elfutils_0.176.6.orig.tar.gz --strip-components=1 -C openresty-elfutils
	cd openresty-elfutils \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
