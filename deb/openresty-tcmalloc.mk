## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_TCMALLOC_VER := 2.9.1

.PHONY: openresty-tcmalloc-download
openresty-tcmalloc-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/gperftools/gperftools/releases/download/gperftools-$(OPENRESTY_TCMALLOC_VER)/gperftools-$(OPENRESTY_TCMALLOC_VER).tar.gz'
	rm -rf openresty-tcmalloc_$(OPENRESTY_TCMALLOC_VER)
	mkdir -p openresty-tcmalloc_$(OPENRESTY_TCMALLOC_VER)
	tar -xf gperftools-$(OPENRESTY_TCMALLOC_VER).tar.gz --strip-components=1 -C openresty-tcmalloc_$(OPENRESTY_TCMALLOC_VER)
	tar -czf openresty-tcmalloc_$(OPENRESTY_TCMALLOC_VER).orig.tar.gz openresty-tcmalloc_$(OPENRESTY_TCMALLOC_VER)

openresty-tcmalloc-clean:
	-cd openresty-tcmalloc && debclean
	-find openresty-tcmalloc -maxdepth 1 ! -name 'debian' ! -name 'openresty-tcmalloc' -print | xargs rm -rf
	rm -rf openresty-tcmalloc*.deb
	rm -rf openresty-tcmalloc_*.*

.PHONY: openresty-tcmalloc-build
openresty-tcmalloc-build: openresty-tcmalloc-clean openresty-tcmalloc-download
	sudo apt-get -y -q install g++ autoconf automake libtool
	sudo apt-get -y -q install --only-upgrade g++ autoconf automake libtool
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-tcmalloc_$(OPENRESTY_TCMALLOC_VER).orig.tar.gz --strip-components=1 -C openresty-tcmalloc
	cd openresty-tcmalloc \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
