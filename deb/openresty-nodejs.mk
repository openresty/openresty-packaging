## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_NODEJS_VER := 15.4.0

.PHONY: openresty-nodejs-download
openresty-nodejs-download:
	wget -nH --cut-dirs=100 --mirror 'https://nodejs.org/dist/v$(OPENRESTY_NODEJS_VER)/node-v$(OPENRESTY_NODEJS_VER).tar.xz'
	rm -rf openresty-nodejs_$(OPENRESTY_NODEJS_VER)
	mkdir -p openresty-nodejs_$(OPENRESTY_NODEJS_VER)
	tar -xf node-v$(OPENRESTY_NODEJS_VER).tar.xz --strip-components=1 -C openresty-nodejs_$(OPENRESTY_NODEJS_VER)
	tar -czf openresty-nodejs_$(OPENRESTY_NODEJS_VER).orig.tar.gz openresty-nodejs_$(OPENRESTY_NODEJS_VER)

openresty-nodejs-clean:
	-cd openresty-nodejs && debclean
	-find openresty-nodejs -maxdepth 1 ! -name 'debian' ! -name 'openresty-nodejs' -print | xargs rm -rf
	rm -rf openresty-nodejs*.deb
	rm -rf openresty-nodejs_*.*

.PHONY: openresty-nodejs-build
openresty-nodejs-build: openresty-nodejs-clean openresty-nodejs-download
	sudo apt-get -y -q install openresty-python3 ccache gcc g++ openresty-saas-zlib-dev libbz2-dev openresty-plus-openssl111-dev
	sudo apt-get -y -q install --only-upgrade openresty-python3 ccache gcc g++ openresty-saas-zlib-dev libbz2-dev openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-nodejs_$(OPENRESTY_NODEJS_VER).orig.tar.gz --strip-components=1 -C openresty-nodejs
	cd openresty-nodejs \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define distro=$(DISTRO) --define arch=$(ARCH) debian/rules.tt2 > debian/rules \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
