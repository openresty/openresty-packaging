## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_B_C_VER := 1.57

.PHONY: openresty-perl-b-c-download
openresty-perl-b-c-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/R/RU/RURBAN/B-C-$(OPENRESTY_PERL_B_C_VER).tar.gz'
	rm -rf openresty-perl-b-c_$(OPENRESTY_PERL_B_C_VER)
	mkdir -p openresty-perl-b-c_$(OPENRESTY_PERL_B_C_VER)
	tar -xf B-C-$(OPENRESTY_PERL_B_C_VER).tar.gz --strip-components=1 -C openresty-perl-b-c_$(OPENRESTY_PERL_B_C_VER)
	tar -czf openresty-perl-b-c_$(OPENRESTY_PERL_B_C_VER).orig.tar.gz openresty-perl-b-c_$(OPENRESTY_PERL_B_C_VER)

openresty-perl-b-c-clean:
	-cd openresty-perl-b-c && debclean
	-find openresty-perl-b-c -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-b-c' -print | xargs rm -rf
	rm -rf openresty-perl-b-c*.deb
	rm -rf openresty-perl-b-c_*.*

.PHONY: openresty-perl-b-c-build
openresty-perl-b-c-build: openresty-perl-b-c-clean openresty-perl-b-c-download
	sudo apt-get -y -q install openresty-perl openresty-perl-b-flags openresty-perl-ipc-run openresty-perl-opcodes openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-b-flags openresty-perl-ipc-run openresty-perl-opcodes openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-b-c_$(OPENRESTY_PERL_B_C_VER).orig.tar.gz --strip-components=1 -C openresty-perl-b-c
	cd openresty-perl-b-c \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
