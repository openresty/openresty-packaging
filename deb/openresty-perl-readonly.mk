## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_READONLY_VER := 2.05

.PHONY: openresty-perl-readonly-download
openresty-perl-readonly-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/S/SA/SANKO/Readonly-$(OPENRESTY_PERL_READONLY_VER).tar.gz'
	rm -rf openresty-perl-readonly_$(OPENRESTY_PERL_READONLY_VER)
	mkdir -p openresty-perl-readonly_$(OPENRESTY_PERL_READONLY_VER)
	tar -xf Readonly-$(OPENRESTY_PERL_READONLY_VER).tar.gz --strip-components=1 -C openresty-perl-readonly_$(OPENRESTY_PERL_READONLY_VER)
	tar -czf openresty-perl-readonly_$(OPENRESTY_PERL_READONLY_VER).orig.tar.gz openresty-perl-readonly_$(OPENRESTY_PERL_READONLY_VER)

openresty-perl-readonly-clean:
	-cd openresty-perl-readonly && debclean
	-find openresty-perl-readonly -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-readonly' -print | xargs rm -rf
	rm -rf openresty-perl-readonly*.deb
	rm -rf openresty-perl-readonly_*.*

.PHONY: openresty-perl-readonly-build
openresty-perl-readonly-build: openresty-perl-readonly-clean openresty-perl-readonly-download
	sudo apt-get -y -q install openresty-perl openresty-perl-module-build-tiny
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-module-build-tiny
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-readonly_$(OPENRESTY_PERL_READONLY_VER).orig.tar.gz --strip-components=1 -C openresty-perl-readonly
	cd openresty-perl-readonly \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
