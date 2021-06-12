## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_IO_SOCKET_SSL_VER := 2.071

.PHONY: openresty-perl-io-socket-ssl-download
openresty-perl-io-socket-ssl-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/S/SU/SULLR/IO-Socket-SSL-$(OPENRESTY_PERL_IO_SOCKET_SSL_VER).tar.gz'
	rm -rf openresty-perl-io-socket-ssl_$(OPENRESTY_PERL_IO_SOCKET_SSL_VER)
	mkdir -p openresty-perl-io-socket-ssl_$(OPENRESTY_PERL_IO_SOCKET_SSL_VER)
	tar -xf IO-Socket-SSL-$(OPENRESTY_PERL_IO_SOCKET_SSL_VER).tar.gz --strip-components=1 -C openresty-perl-io-socket-ssl_$(OPENRESTY_PERL_IO_SOCKET_SSL_VER)
	tar -czf openresty-perl-io-socket-ssl_$(OPENRESTY_PERL_IO_SOCKET_SSL_VER).orig.tar.gz openresty-perl-io-socket-ssl_$(OPENRESTY_PERL_IO_SOCKET_SSL_VER)

openresty-perl-io-socket-ssl-clean:
	-cd openresty-perl-io-socket-ssl && debclean
	-find openresty-perl-io-socket-ssl -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-io-socket-ssl' -print | xargs rm -rf
	rm -rf openresty-perl-io-socket-ssl*.deb
	rm -rf openresty-perl-io-socket-ssl_*.*

.PHONY: openresty-perl-io-socket-ssl-build
openresty-perl-io-socket-ssl-build: openresty-perl-io-socket-ssl-clean openresty-perl-io-socket-ssl-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-io-socket-ssl_$(OPENRESTY_PERL_IO_SOCKET_SSL_VER).orig.tar.gz --strip-components=1 -C openresty-perl-io-socket-ssl
	cd openresty-perl-io-socket-ssl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
