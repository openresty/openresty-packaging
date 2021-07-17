SSL111_VER=1.1.1k

.PHONY: openresty-plus-openssl111-download
openresty-plus-openssl111-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(SSL111_VER).tar.gz'
	cp openssl-$(SSL111_VER).tar.gz openresty-plus-openssl111_$(SSL111_VER).orig.tar.gz

.PHONY: openresty-plus-openssl111-build
openresty-plus-openssl111-build: | openresty-plus-openssl111-clean openresty-plus-openssl111-download
	sudo apt-get -y -qq install openresty-zlib-dev
	sudo apt-get --only-upgrade -y -qq install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-openssl111_$(SSL111_VER).orig.tar.gz --strip-components=1 -C openresty-plus-openssl111
	cd openresty-plus-openssl111 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty-plus-openssl111*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-plus-openssl111-clean
openresty-plus-openssl111-clean:
	sudo apt-get -y -qq install openresty-zlib-dev
	-cd openresty-plus-openssl111 && debclean
	rm -rf openresty-plus-openssl111/debian/tmp openresty-plus-openssl111/test openresty-plus-openssl111/*.a
	find openresty-plus-openssl111 -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-openssl111' -print | xargs rm -rf
	rm -f openresty-plus-openssl111*.deb
	rm -f openresty-plus-openssl111_*.*
