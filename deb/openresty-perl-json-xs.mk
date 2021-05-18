## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_JSON_XS_VER := 4.03

.PHONY: openresty-perl-json-xs-download
openresty-perl-json-xs-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/JSON-XS-$(OPENRESTY_PERL_JSON_XS_VER).tar.gz'
	rm -rf openresty-perl-json-xs_$(OPENRESTY_PERL_JSON_XS_VER)
	mkdir -p openresty-perl-json-xs_$(OPENRESTY_PERL_JSON_XS_VER)
	tar -xf JSON-XS-$(OPENRESTY_PERL_JSON_XS_VER).tar.gz --strip-components=1 -C openresty-perl-json-xs_$(OPENRESTY_PERL_JSON_XS_VER)
	tar -czf openresty-perl-json-xs_$(OPENRESTY_PERL_JSON_XS_VER).orig.tar.gz openresty-perl-json-xs_$(OPENRESTY_PERL_JSON_XS_VER)

openresty-perl-json-xs-clean:
	-cd openresty-perl-json-xs && debclean
	-find openresty-perl-json-xs -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-json-xs' -print | xargs rm -rf
	rm -rf openresty-perl-json-xs*.deb
	rm -rf openresty-perl-json-xs_*.*

.PHONY: openresty-perl-json-xs-build
openresty-perl-json-xs-build: openresty-perl-json-xs-clean openresty-perl-json-xs-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev openresty-perl-types-serialiser openresty-perl-common-sense openresty-perl-canary-stability
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev openresty-perl-types-serialiser openresty-perl-common-sense openresty-perl-canary-stability
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-json-xs_$(OPENRESTY_PERL_JSON_XS_VER).orig.tar.gz --strip-components=1 -C openresty-perl-json-xs
	cd openresty-perl-json-xs \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
