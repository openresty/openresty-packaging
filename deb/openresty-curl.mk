## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_CURL_VER := 7.63.0

.PHONY: openresty-curl-download
openresty-curl-download:
	wget -nH --cut-dirs=100 --mirror 'https://curl.se/download/curl-$(OPENRESTY_CURL_VER).tar.gz'
	rm -rf openresty-curl_$(OPENRESTY_CURL_VER)
	mkdir -p openresty-curl_$(OPENRESTY_CURL_VER)
	tar -xf curl-$(OPENRESTY_CURL_VER).tar.gz --strip-components=1 -C openresty-curl_$(OPENRESTY_CURL_VER)
	tar -czf openresty-curl_$(OPENRESTY_CURL_VER).orig.tar.gz openresty-curl_$(OPENRESTY_CURL_VER)

openresty-curl-clean:
	-cd openresty-curl && debclean
	-find openresty-curl -maxdepth 1 ! -name 'debian' ! -name 'openresty-curl' -print | xargs rm -rf
	rm -rf openresty-curl*.deb
	rm -rf openresty-curl_*.*

.PHONY: openresty-curl-build
openresty-curl-build: openresty-curl-clean openresty-curl-download
	sudo apt-get -y -q install automake libbrotli-dev coreutils gcc groff libkrb5-dev libidn2-0-dev libnghttp2-dev libpsl-dev libssh-dev libtool make libldap2-dev openssh-client openssh-server libssl-dev pkg-config python3-dev sed zlib1g-dev perl
	sudo apt-get -y -q install --only-upgrade automake libbrotli-dev coreutils gcc groff libkrb5-dev libidn2-0-dev libnghttp2-dev libpsl-dev libssh-dev libtool make libldap2-dev openssh-client openssh-server libssl-dev pkg-config python3-dev sed zlib1g-dev perl
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-curl_$(OPENRESTY_CURL_VER).orig.tar.gz --strip-components=1 -C openresty-curl
	cd openresty-curl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
