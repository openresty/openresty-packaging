## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_B_FLAGS_VER := 0.17

.PHONY: openresty-perl-b-flags-download
openresty-perl-b-flags-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/R/RU/RURBAN/B-Flags-$(OPENRESTY_PERL_B_FLAGS_VER).tar.gz'
	rm -rf openresty-perl-b-flags_$(OPENRESTY_PERL_B_FLAGS_VER)
	mkdir -p openresty-perl-b-flags_$(OPENRESTY_PERL_B_FLAGS_VER)
	tar -xf B-Flags-$(OPENRESTY_PERL_B_FLAGS_VER).tar.gz --strip-components=1 -C openresty-perl-b-flags_$(OPENRESTY_PERL_B_FLAGS_VER)
	tar -czf openresty-perl-b-flags_$(OPENRESTY_PERL_B_FLAGS_VER).orig.tar.gz openresty-perl-b-flags_$(OPENRESTY_PERL_B_FLAGS_VER)

.PHONY: openresty-perl-b-flags-clean
openresty-perl-b-flags-clean:
	-cd openresty-perl-b-flags && debclean
	-find openresty-perl-b-flags -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-b-flags' -print | xargs rm -rf
	rm -rf openresty-perl-b-flags*.deb
	rm -rf openresty-perl-b-flags_*.*

.PHONY: openresty-perl-B-Flags-build
openresty-perl-B-Flags-build: openresty-perl-b-flags-build

.PHONY: openresty-perl-b-flags-build
openresty-perl-b-flags-build: openresty-perl-b-flags-clean openresty-perl-b-flags-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-b-flags_$(OPENRESTY_PERL_B_FLAGS_VER).orig.tar.gz --strip-components=1 -C openresty-perl-b-flags
	cd openresty-perl-b-flags \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
