## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_VER := 5.24.4

.PHONY: openresty-perl-download
openresty-perl-download:
	wget -nH --cut-dirs=100 --mirror 'https://www.cpan.org/src/5.0/perl-$(OPENRESTY_PERL_VER).tar.gz'
	rm -rf openresty-perl_$(OPENRESTY_PERL_VER)
	mkdir -p openresty-perl_$(OPENRESTY_PERL_VER)
	tar -xf perl-$(OPENRESTY_PERL_VER).tar.gz --strip-components=1 -C openresty-perl_$(OPENRESTY_PERL_VER)
	tar -czf openresty-perl_$(OPENRESTY_PERL_VER).orig.tar.gz openresty-perl_$(OPENRESTY_PERL_VER)

openresty-perl-clean:
	-cd openresty-perl && debclean
	-find openresty-perl -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl' -print | xargs rm -rf
	rm -rf openresty-perl*.deb
	rm -rf openresty-perl_*.*

.PHONY: openresty-perl-build
openresty-perl-build: openresty-perl-clean openresty-perl-download
	sudo apt-get -y -q install ccache gcc gawk sed procps zlib1g-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc gawk sed procps zlib1g-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl_$(OPENRESTY_PERL_VER).orig.tar.gz --strip-components=1 -C openresty-perl
	cd openresty-perl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
