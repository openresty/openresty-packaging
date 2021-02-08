## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_MODULE_BUILD_TINY_VER := 0.039

.PHONY: openresty-perl-module-build-tiny-download
openresty-perl-module-build-tiny-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-Tiny-$(OPENRESTY_PERL_MODULE_BUILD_TINY_VER).tar.gz'
	rm -rf openresty-perl-module-build-tiny_$(OPENRESTY_PERL_MODULE_BUILD_TINY_VER)
	mkdir -p openresty-perl-module-build-tiny_$(OPENRESTY_PERL_MODULE_BUILD_TINY_VER)
	tar -xf Module-Build-Tiny-$(OPENRESTY_PERL_MODULE_BUILD_TINY_VER).tar.gz --strip-components=1 -C openresty-perl-module-build-tiny_$(OPENRESTY_PERL_MODULE_BUILD_TINY_VER)
	tar -czf openresty-perl-module-build-tiny_$(OPENRESTY_PERL_MODULE_BUILD_TINY_VER).orig.tar.gz openresty-perl-module-build-tiny_$(OPENRESTY_PERL_MODULE_BUILD_TINY_VER)

openresty-perl-module-build-tiny-clean:
	-cd openresty-perl-module-build-tiny && debclean
	-find openresty-perl-module-build-tiny -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-module-build-tiny' -print | xargs rm -rf
	rm -rf openresty-perl-module-build-tiny*.deb
	rm -rf openresty-perl-module-build-tiny_*.*

.PHONY: openresty-perl-module-build-tiny-build
openresty-perl-module-build-tiny-build: openresty-perl-module-build-tiny-clean openresty-perl-module-build-tiny-download
	sudo apt-get -y -q install openresty-perl openresty-perl-extutils-config openresty-perl-extutils-helpers openresty-perl-extutils-installpaths
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-extutils-config openresty-perl-extutils-helpers openresty-perl-extutils-installpaths
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-module-build-tiny_$(OPENRESTY_PERL_MODULE_BUILD_TINY_VER).orig.tar.gz --strip-components=1 -C openresty-perl-module-build-tiny
	cd openresty-perl-module-build-tiny \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
