## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_TYPES_SERIALISER_VER := 1.01

.PHONY: openresty-perl-types-serialiser-download
openresty-perl-types-serialiser-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Types-Serialiser-$(OPENRESTY_PERL_TYPES_SERIALISER_VER).tar.gz'
	rm -rf openresty-perl-types-serialiser_$(OPENRESTY_PERL_TYPES_SERIALISER_VER)
	mkdir -p openresty-perl-types-serialiser_$(OPENRESTY_PERL_TYPES_SERIALISER_VER)
	tar -xf Types-Serialiser-$(OPENRESTY_PERL_TYPES_SERIALISER_VER).tar.gz --strip-components=1 -C openresty-perl-types-serialiser_$(OPENRESTY_PERL_TYPES_SERIALISER_VER)
	tar -czf openresty-perl-types-serialiser_$(OPENRESTY_PERL_TYPES_SERIALISER_VER).orig.tar.gz openresty-perl-types-serialiser_$(OPENRESTY_PERL_TYPES_SERIALISER_VER)

openresty-perl-types-serialiser-clean:
	-cd openresty-perl-types-serialiser && debclean
	-find openresty-perl-types-serialiser -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-types-serialiser' -print | xargs rm -rf
	rm -rf openresty-perl-types-serialiser*.deb
	rm -rf openresty-perl-types-serialiser_*.*

.PHONY: openresty-perl-types-serialiser-build
openresty-perl-types-serialiser-build: openresty-perl-types-serialiser-clean openresty-perl-types-serialiser-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev openresty-perl-common-sense
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev openresty-perl-common-sense
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-types-serialiser_$(OPENRESTY_PERL_TYPES_SERIALISER_VER).orig.tar.gz --strip-components=1 -C openresty-perl-types-serialiser
	cd openresty-perl-types-serialiser \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
