## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_APP_CPANMINUS_VER := 1.7044

.PHONY: openresty-perl-app-cpanminus-download
openresty-perl-app-cpanminus-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/App-cpanminus-$(OPENRESTY_PERL_APP_CPANMINUS_VER).tar.gz'
	rm -rf openresty-perl-app-cpanminus_$(OPENRESTY_PERL_APP_CPANMINUS_VER)
	mkdir -p openresty-perl-app-cpanminus_$(OPENRESTY_PERL_APP_CPANMINUS_VER)
	tar -xf App-cpanminus-$(OPENRESTY_PERL_APP_CPANMINUS_VER).tar.gz --strip-components=1 -C openresty-perl-app-cpanminus_$(OPENRESTY_PERL_APP_CPANMINUS_VER)
	tar -czf openresty-perl-app-cpanminus_$(OPENRESTY_PERL_APP_CPANMINUS_VER).orig.tar.gz openresty-perl-app-cpanminus_$(OPENRESTY_PERL_APP_CPANMINUS_VER)

openresty-perl-app-cpanminus-clean:
	-cd openresty-perl-app-cpanminus && debclean
	-find openresty-perl-app-cpanminus -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-app-cpanminus' -print | xargs rm -rf
	rm -rf openresty-perl-app-cpanminus*.deb
	rm -rf openresty-perl-app-cpanminus_*.*

.PHONY: openresty-perl-app-cpanminus-build
openresty-perl-app-cpanminus-build: openresty-perl-app-cpanminus-clean openresty-perl-app-cpanminus-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-app-cpanminus_$(OPENRESTY_PERL_APP_CPANMINUS_VER).orig.tar.gz --strip-components=1 -C openresty-perl-app-cpanminus
	cd openresty-perl-app-cpanminus \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
