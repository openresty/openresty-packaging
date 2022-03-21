.PHONY: openresty-plus-openssl111-debug-download
openresty-plus-openssl111-debug-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(SSL111_VER).tar.gz'
	cp openssl-$(SSL111_VER).tar.gz openresty-plus-openssl111-debug_$(SSL111_VER).orig.tar.gz

.PHONY: openresty-plus-openssl111-debug-build
openresty-plus-openssl111-debug-build: | openresty-plus-openssl111-debug-clean openresty-plus-openssl111-debug-download
	sudo apt-get -y -qq install openresty-zlib-dev
	sudo apt-get -y -qq --only-upgrade install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-openssl111-debug_$(SSL111_VER).orig.tar.gz --strip-components=1 -C openresty-plus-openssl111-debug
	cd openresty-plus-openssl111-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild -sa $(OPTS) -j$(JOBS)
	#for f in openresty-plus-openssl111-debug*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-plus-openssl111-debug-clean
openresty-plus-openssl111-debug-clean:
	sudo apt-get -y -qq install openresty-zlib-dev
	-cd openresty-plus-openssl111-debug && debclean
	rm -rf openresty-plus-openssl111-debug/debian/tmp openresty-plus-openssl111-debug/test openresty-plus-openssl111-debug/*.a
	find openresty-plus-openssl111-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-openssl111-debug' -print | xargs rm -rf
	rm -f openresty-plus-openssl111*.deb
	rm -f openresty-plus-openssl111-debug_*.*
