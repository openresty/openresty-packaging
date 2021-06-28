## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER := 0.26

.PHONY: openresty-perl-protocol-websocket-download
openresty-perl-protocol-websocket-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/V/VT/VTI/Protocol-WebSocket-$(OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER).tar.gz'
	rm -rf openresty-perl-protocol-websocket_$(OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER)
	mkdir -p openresty-perl-protocol-websocket_$(OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER)
	tar -xf Protocol-WebSocket-$(OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER).tar.gz --strip-components=1 -C openresty-perl-protocol-websocket_$(OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER)
	tar -czf openresty-perl-protocol-websocket_$(OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER).orig.tar.gz openresty-perl-protocol-websocket_$(OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER)

openresty-perl-protocol-websocket-clean:
	-cd openresty-perl-protocol-websocket && debclean
	-find openresty-perl-protocol-websocket -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-protocol-websocket' -print | xargs rm -rf
	rm -rf openresty-perl-protocol-websocket*.deb
	rm -rf openresty-perl-protocol-webSocket_*.*

.PHONY: openresty-perl-protocol-websocket-build
openresty-perl-protocol-websocket-build: openresty-perl-protocol-websocket-clean openresty-perl-protocol-websocket-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev openresty-perl-module-build-tiny
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev openresty-perl-module-build-tiny
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-protocol-websocket_$(OPENRESTY_PERL_PROTOCOL_WEBSOCKET_VER).orig.tar.gz --strip-components=1 -C openresty-perl-protocol-websocket
	cd openresty-perl-protocol-websocket \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
