## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_MOZILLA_CA_VER := 20200520

.PHONY: openresty-perl-mozilla-ca-download
openresty-perl-mozilla-ca-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/A/AB/ABH/Mozilla-CA-$(OPENRESTY_PERL_MOZILLA_CA_VER).tar.gz'
	rm -rf openresty-perl-mozilla-ca_$(OPENRESTY_PERL_MOZILLA_CA_VER)
	mkdir -p openresty-perl-mozilla-ca_$(OPENRESTY_PERL_MOZILLA_CA_VER)
	tar -xf Mozilla-CA-$(OPENRESTY_PERL_MOZILLA_CA_VER).tar.gz --strip-components=1 -C openresty-perl-mozilla-ca_$(OPENRESTY_PERL_MOZILLA_CA_VER)
	tar -czf openresty-perl-mozilla-ca_$(OPENRESTY_PERL_MOZILLA_CA_VER).orig.tar.gz openresty-perl-mozilla-ca_$(OPENRESTY_PERL_MOZILLA_CA_VER)

openresty-perl-mozilla-ca-clean:
	-cd openresty-perl-mozilla-ca && debclean
	-find openresty-perl-mozilla-ca -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-mozilla-ca' -print | xargs rm -rf
	rm -rf openresty-perl-mozilla-ca*.deb
	rm -rf openresty-perl-mozilla-ca_*

.PHONY: openresty-perl-mozilla-ca-build
openresty-perl-mozilla-ca-build: openresty-perl-mozilla-ca-clean openresty-perl-mozilla-ca-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-mozilla-ca_$(OPENRESTY_PERL_MOZILLA_CA_VER).orig.tar.gz --strip-components=1 -C openresty-perl-mozilla-ca
	cd openresty-perl-mozilla-ca \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
