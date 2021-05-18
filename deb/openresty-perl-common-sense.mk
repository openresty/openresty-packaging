## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_COMMON_SENSE_VER := 3.75

.PHONY: openresty-perl-common-sense-download
openresty-perl-common-sense-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/common-sense-$(OPENRESTY_PERL_COMMON_SENSE_VER).tar.gz'
	rm -rf openresty-perl-common-sense_$(OPENRESTY_PERL_COMMON_SENSE_VER)
	mkdir -p openresty-perl-common-sense_$(OPENRESTY_PERL_COMMON_SENSE_VER)
	tar -xf common-sense-$(OPENRESTY_PERL_COMMON_SENSE_VER).tar.gz --strip-components=1 -C openresty-perl-common-sense_$(OPENRESTY_PERL_COMMON_SENSE_VER)
	tar -czf openresty-perl-common-sense_$(OPENRESTY_PERL_COMMON_SENSE_VER).orig.tar.gz openresty-perl-common-sense_$(OPENRESTY_PERL_COMMON_SENSE_VER)

openresty-perl-common-sense-clean:
	-cd openresty-perl-common-sense && debclean
	-find openresty-perl-common-sense -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-common-sense' -print | xargs rm -rf
	rm -rf openresty-perl-common-sense*.deb
	rm -rf openresty-perl-common-sense_*.*

.PHONY: openresty-perl-common-sense-build
openresty-perl-common-sense-build: openresty-perl-common-sense-clean openresty-perl-common-sense-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-common-sense_$(OPENRESTY_PERL_COMMON_SENSE_VER).orig.tar.gz --strip-components=1 -C openresty-perl-common-sense
	cd openresty-perl-common-sense \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
