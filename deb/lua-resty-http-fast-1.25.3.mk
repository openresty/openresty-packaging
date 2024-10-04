## Author: spec2deb.pl
### Version: 0.01

LUA_RESTY_HTTP_FAST_VER := 0.0.1

.PHONY: lua-resty-http-fast-1.25.3-download
lua-resty-http-fast-1.25.3-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-resty-http-fast-$(LUA_RESTY_HTTP_FAST_VER).tar.gz ./
	rm -rf lua-resty-http-fast-1.25.3_$(LUA_RESTY_HTTP_FAST_VER)
	mkdir -p lua-resty-http-fast-1.25.3_$(LUA_RESTY_HTTP_FAST_VER)
	tar -xf lua-resty-http-fast-$(LUA_RESTY_HTTP_FAST_VER).tar.gz --strip-components=1 -C lua-resty-http-fast-1.25.3_$(LUA_RESTY_HTTP_FAST_VER)
	tar -czf lua-resty-http-fast-1.25.3_$(LUA_RESTY_HTTP_FAST_VER).orig.tar.gz lua-resty-http-fast-1.25.3_$(LUA_RESTY_HTTP_FAST_VER)

lua-resty-http-fast-1.25.3-clean:
	-cd lua-resty-http-fast-1.25.3 && debclean
	-find lua-resty-http-fast-1.25.3 -maxdepth 1 ! -name 'debian' ! -name 'lua-resty-http-fast-1.25.3' -print | xargs rm -rf
	rm -rf lua-resty-http-fast-1.25.3*.deb
	rm -rf lua-resty-http-fast-1.25.3_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: lua-resty-http-fast-1.25.3-build
lua-resty-http-fast-1.25.3-build: lua-resty-http-fast-1.25.3-clean lua-resty-http-fast-1.25.3-download
	sudo apt-get -y -q install openresty
	sudo apt-get -y -q install --only-upgrade openresty
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf lua-resty-http-fast-1.25.3_$(LUA_RESTY_HTTP_FAST_VER).orig.tar.gz --strip-components=1 -C lua-resty-http-fast-1.25.3
	cd lua-resty-http-fast-1.25.3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
