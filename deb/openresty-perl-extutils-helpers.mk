## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_EXTUTILS_HELPERS_VER := 0.026

.PHONY: openresty-perl-extutils-helpers-download
openresty-perl-extutils-helpers-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Helpers-$(OPENRESTY_PERL_EXTUTILS_HELPERS_VER).tar.gz'
	rm -rf openresty-perl-extutils-helpers_$(OPENRESTY_PERL_EXTUTILS_HELPERS_VER)
	mkdir -p openresty-perl-extutils-helpers_$(OPENRESTY_PERL_EXTUTILS_HELPERS_VER)
	tar -xf ExtUtils-Helpers-$(OPENRESTY_PERL_EXTUTILS_HELPERS_VER).tar.gz --strip-components=1 -C openresty-perl-extutils-helpers_$(OPENRESTY_PERL_EXTUTILS_HELPERS_VER)
	tar -czf openresty-perl-extutils-helpers_$(OPENRESTY_PERL_EXTUTILS_HELPERS_VER).orig.tar.gz openresty-perl-extutils-helpers_$(OPENRESTY_PERL_EXTUTILS_HELPERS_VER)

openresty-perl-extutils-helpers-clean:
	-cd openresty-perl-extutils-helpers && debclean
	-find openresty-perl-extutils-helpers -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-extutils-helpers' -print | xargs rm -rf
	rm -rf openresty-perl-extutils-helpers*.deb
	rm -rf openresty-perl-extutils-helpers_*.*

.PHONY: openresty-perl-extutils-helpers-build
openresty-perl-extutils-helpers-build: openresty-perl-extutils-helpers-clean openresty-perl-extutils-helpers-download
	sudo apt-get -y -q install openresty-perl
	sudo apt-get -y -q install --only-upgrade openresty-perl
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-extutils-helpers_$(OPENRESTY_PERL_EXTUTILS_HELPERS_VER).orig.tar.gz --strip-components=1 -C openresty-perl-extutils-helpers
		cd openresty-perl-extutils-helpers \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
