## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_CANARY_STABILITY_VER := 2013

.PHONY: openresty-perl-canary-stability-download
openresty-perl-canary-stability-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Canary-Stability-$(OPENRESTY_PERL_CANARY_STABILITY_VER).tar.gz'
	rm -rf openresty-perl-canary-stability_$(OPENRESTY_PERL_CANARY_STABILITY_VER)
	mkdir -p openresty-perl-canary-stability_$(OPENRESTY_PERL_CANARY_STABILITY_VER)
	tar -xf Canary-Stability-$(OPENRESTY_PERL_CANARY_STABILITY_VER).tar.gz --strip-components=1 -C openresty-perl-canary-stability_$(OPENRESTY_PERL_CANARY_STABILITY_VER)
	tar -czf openresty-perl-canary-stability_$(OPENRESTY_PERL_CANARY_STABILITY_VER).orig.tar.gz openresty-perl-canary-stability_$(OPENRESTY_PERL_CANARY_STABILITY_VER)

openresty-perl-canary-stability-clean:
	-cd openresty-perl-canary-stability && debclean
	-find openresty-perl-canary-stability -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-canary-stability' -print | xargs rm -rf
	rm -rf openresty-perl-canary-stability*.deb
	rm -rf openresty-perl-canary-stability_*.*

.PHONY: openresty-perl-canary-stability-build
openresty-perl-canary-stability-build: openresty-perl-canary-stability-clean openresty-perl-canary-stability-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-canary-stability_$(OPENRESTY_PERL_CANARY_STABILITY_VER).orig.tar.gz --strip-components=1 -C openresty-perl-canary-stability
	cd openresty-perl-canary-stability \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
