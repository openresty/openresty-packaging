## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LUA_CJSON_VER := 2.1.0.13.3

.PHONY: openresty-lua-cjson-download
openresty-lua-cjson-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-cjson-plus-$(OPENRESTY_LUA_CJSON_VER).tar.gz ./
	rm -rf openresty-lua-cjson_$(OPENRESTY_LUA_CJSON_VER)
	mkdir -p openresty-lua-cjson_$(OPENRESTY_LUA_CJSON_VER)
	tar -xf lua-cjson-plus-$(OPENRESTY_LUA_CJSON_VER).tar.gz --strip-components=1 -C openresty-lua-cjson_$(OPENRESTY_LUA_CJSON_VER)
	tar -czf openresty-lua-cjson_$(OPENRESTY_LUA_CJSON_VER).orig.tar.gz openresty-lua-cjson_$(OPENRESTY_LUA_CJSON_VER)

openresty-lua-cjson-clean:
	-cd openresty-lua-cjson && debclean
	-find openresty-lua-cjson -maxdepth 1 ! -name 'debian' ! -name 'openresty-lua-cjson' -print | xargs rm -rf
	rm -rf openresty-lua-cjson*.deb
	rm -rf openresty-lua-cjson_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-lua-cjson-build
openresty-lua-cjson-build: openresty-lua-cjson-clean openresty-lua-cjson-download
	sudo apt-get -y -q install libtool openresty
	sudo apt-get -y -q install --only-upgrade libtool openresty
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-lua-cjson_$(OPENRESTY_LUA_CJSON_VER).orig.tar.gz --strip-components=1 -C openresty-lua-cjson
	cd openresty-lua-cjson \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
