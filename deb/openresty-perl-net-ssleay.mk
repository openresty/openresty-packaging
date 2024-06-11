## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_NET_SSLEAY_VER := 1.90

.PHONY: openresty-perl-net-ssleay-download
openresty-perl-net-ssleay-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/C/CH/CHRISN/Net-SSLeay-$(OPENRESTY_PERL_NET_SSLEAY_VER).tar.gz'
	rm -rf openresty-perl-net-ssleay_$(OPENRESTY_PERL_NET_SSLEAY_VER)
	mkdir -p openresty-perl-net-ssleay_$(OPENRESTY_PERL_NET_SSLEAY_VER)
	tar -xf Net-SSLeay-$(OPENRESTY_PERL_NET_SSLEAY_VER).tar.gz --strip-components=1 -C openresty-perl-net-ssleay_$(OPENRESTY_PERL_NET_SSLEAY_VER)
	tar -czf openresty-perl-net-ssleay_$(OPENRESTY_PERL_NET_SSLEAY_VER).orig.tar.gz openresty-perl-net-ssleay_$(OPENRESTY_PERL_NET_SSLEAY_VER)

openresty-perl-net-ssleay-clean:
	-cd openresty-perl-net-ssleay && debclean
	-find openresty-perl-net-ssleay -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-net-ssleay' -print | xargs rm -rf
	rm -rf openresty-perl-net-ssleay*.deb
	rm -rf openresty-perl-net-ssleay_*.*

.PHONY: openresty-perl-net-ssleay-build
openresty-perl-net-ssleay-build: openresty-perl-net-ssleay-clean openresty-perl-net-ssleay-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev openresty-plus-openssl111-dev zlib1g-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev openresty-plus-openssl111-dev zlib1g-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-net-ssleay_$(OPENRESTY_PERL_NET_SSLEAY_VER).orig.tar.gz --strip-components=1 -C openresty-perl-net-ssleay
	cd openresty-perl-net-ssleay \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
