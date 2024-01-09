## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_POSTGRESQL12_VER := 12.5

.PHONY: openresty-postgresql12-download
openresty-postgresql12-download:
	wget -nH --cut-dirs=100 --mirror 'https://ftp.postgresql.org/pub/source/v$(OPENRESTY_POSTGRESQL12_VER)/postgresql-$(OPENRESTY_POSTGRESQL12_VER).tar.gz'
	rm -rf openresty-postgresql12_$(OPENRESTY_POSTGRESQL12_VER)
	mkdir -p openresty-postgresql12_$(OPENRESTY_POSTGRESQL12_VER)
	tar -xf postgresql-$(OPENRESTY_POSTGRESQL12_VER).tar.gz --strip-components=1 -C openresty-postgresql12_$(OPENRESTY_POSTGRESQL12_VER)
	tar -I 'gzip -1' -cf openresty-postgresql12_$(OPENRESTY_POSTGRESQL12_VER).orig.tar.gz openresty-postgresql12_$(OPENRESTY_POSTGRESQL12_VER)

openresty-postgresql12-clean:
	-cd openresty-postgresql12 && debclean
	-find openresty-postgresql12 -maxdepth 1 ! -name 'debian' ! -name 'openresty-postgresql12' -print | xargs rm -rf
	rm -rf openresty-postgresql12*.deb
	rm -rf openresty-postgresql12_*.*

.PHONY: openresty-postgresql12-build
openresty-postgresql12-build: openresty-postgresql12-clean openresty-postgresql12-download
	sudo apt-get -y -q install ccache libxml2-dev libxslt-dev libossp-uuid-dev libreadline-dev openresty-plus-openssl111-dev bison
	sudo apt-get -y -q install --only-upgrade ccache libxml2-dev libxslt-dev libossp-uuid-dev libreadline-dev openresty-plus-openssl111-dev bison
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-postgresql12_$(OPENRESTY_POSTGRESQL12_VER).orig.tar.gz --strip-components=1 -C openresty-postgresql12
	cd openresty-postgresql12 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
