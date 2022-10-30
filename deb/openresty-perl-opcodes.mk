## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_OPCODES_VER := 0.14

.PHONY: openresty-perl-opcodes-download
openresty-perl-opcodes-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Opcodes-$(OPENRESTY_PERL_OPCODES_VER).tar.gz'
	rm -rf openresty-perl-opcodes_$(OPENRESTY_PERL_OPCODES_VER)
	mkdir -p openresty-perl-opcodes_$(OPENRESTY_PERL_OPCODES_VER)
	tar -xf Opcodes-$(OPENRESTY_PERL_OPCODES_VER).tar.gz --strip-components=1 -C openresty-perl-opcodes_$(OPENRESTY_PERL_OPCODES_VER)
	tar -czf openresty-perl-opcodes_$(OPENRESTY_PERL_OPCODES_VER).orig.tar.gz openresty-perl-opcodes_$(OPENRESTY_PERL_OPCODES_VER)

.PHONY: openresty-perl-opcodes-clean
openresty-perl-opcodes-clean:
	-cd openresty-perl-opcodes && debclean
	-find openresty-perl-opcodes -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-opcodes' -print | xargs rm -rf
	rm -rf openresty-perl-opcodes*.deb
	rm -rf openresty-perl-opcodes_*.*

.PHONY: openresty-perl-Opcodes-build
openresty-perl-Opcodes-build: openresty-perl-opcodes-build

.PHONY: openresty-perl-opcodes-build
openresty-perl-opcodes-build: openresty-perl-opcodes-clean openresty-perl-opcodes-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-opcodes_$(OPENRESTY_PERL_OPCODES_VER).orig.tar.gz --strip-components=1 -C openresty-perl-opcodes
	cd openresty-perl-opcodes \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
