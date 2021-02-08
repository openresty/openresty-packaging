## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_EXTUTILS_CONFIG_VER := 0.008

.PHONY: openresty-perl-extutils-config-download
openresty-perl-extutils-config-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Config-$(OPENRESTY_PERL_EXTUTILS_CONFIG_VER).tar.gz'
	rm -rf openresty-perl-extutils-config_$(OPENRESTY_PERL_EXTUTILS_CONFIG_VER)
	mkdir -p openresty-perl-extutils-config_$(OPENRESTY_PERL_EXTUTILS_CONFIG_VER)
	tar -xf ExtUtils-Config-$(OPENRESTY_PERL_EXTUTILS_CONFIG_VER).tar.gz --strip-components=1 -C openresty-perl-extutils-config_$(OPENRESTY_PERL_EXTUTILS_CONFIG_VER)
	tar -czf openresty-perl-extutils-config_$(OPENRESTY_PERL_EXTUTILS_CONFIG_VER).orig.tar.gz openresty-perl-extutils-config_$(OPENRESTY_PERL_EXTUTILS_CONFIG_VER)

openresty-perl-extutils-config-clean:
	-cd openresty-perl-extutils-config && debclean
	-find openresty-perl-extutils-config -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-extutils-config' -print | xargs rm -rf
	rm -rf openresty-perl-extutils-config*.deb
	rm -rf openresty-perl-extutils-config_*.*

.PHONY: openresty-perl-extutils-config-build
openresty-perl-extutils-config-build: openresty-perl-extutils-config-clean openresty-perl-extutils-config-download
	sudo apt-get -y -q install openresty-perl
	sudo apt-get -y -q install --only-upgrade openresty-perl
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-extutils-config_$(OPENRESTY_PERL_EXTUTILS_CONFIG_VER).orig.tar.gz --strip-components=1 -C openresty-perl-extutils-config
	cd openresty-perl-extutils-config \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
