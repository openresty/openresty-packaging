## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER := 0.012

.PHONY: openresty-perl-extutils-installpaths-download
openresty-perl-extutils-installpaths-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-InstallPaths-$(OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER).tar.gz'
	rm -rf openresty-perl-extutils-installpaths_$(OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER)
	mkdir -p openresty-perl-extutils-installpaths_$(OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER)
	tar -xf ExtUtils-InstallPaths-$(OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER).tar.gz --strip-components=1 -C openresty-perl-extutils-installpaths_$(OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER)
	tar -czf openresty-perl-extutils-installpaths_$(OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER).orig.tar.gz openresty-perl-extutils-installpaths_$(OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER)

openresty-perl-extutils-installpaths-clean:
	-cd openresty-perl-extutils-installpaths && debclean
	-find openresty-perl-extutils-installpaths -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-extutils-installpaths' -print | xargs rm -rf
	rm -rf openresty-perl-extutils-installpaths*.deb
	rm -rf openresty-perl-extutils-installpaths_*.*

.PHONY: openresty-perl-extutils-installpaths-build
openresty-perl-extutils-installpaths-build: openresty-perl-extutils-installpaths-clean openresty-perl-extutils-installpaths-download
	sudo apt-get -y -q install openresty-perl openresty-perl-extutils-config
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-extutils-config
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-extutils-installpaths_$(OPENRESTY_PERL_EXTUTILS_INSTALLPATHS_VER).orig.tar.gz --strip-components=1 -C openresty-perl-extutils-installpaths
	cd openresty-perl-extutils-installpaths \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
