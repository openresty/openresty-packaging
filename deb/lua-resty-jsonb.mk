## Author: spec2deb.pl
### Version: 0.01

LUA_RESTY_JSONB_VER := 0.0.4

.PHONY: lua-resty-jsonb-download
lua-resty-jsonb-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-resty-jsonb-$(LUA_RESTY_JSONB_VER).tar.gz ./
	rm -rf lua-resty-jsonb_$(LUA_RESTY_JSONB_VER)
	mkdir -p lua-resty-jsonb_$(LUA_RESTY_JSONB_VER)
	tar -xf lua-resty-jsonb-$(LUA_RESTY_JSONB_VER).tar.gz --strip-components=1 -C lua-resty-jsonb_$(LUA_RESTY_JSONB_VER)
	tar -czf lua-resty-jsonb_$(LUA_RESTY_JSONB_VER).orig.tar.gz lua-resty-jsonb_$(LUA_RESTY_JSONB_VER)

lua-resty-jsonb-clean:
	-cd lua-resty-jsonb && debclean
	-find lua-resty-jsonb -maxdepth 1 ! -name 'debian' ! -name 'lua-resty-jsonb' -print | xargs rm -rf
	rm -rf lua-resty-jsonb*.deb
	rm -rf lua-resty-jsonb_*.*

.PHONY: lua-resty-jsonb-build
lua-resty-jsonb-build: lua-resty-jsonb-clean lua-resty-jsonb-download
	sudo apt-get -y -q install gcc make openresty-yajl-dev openresty
	sudo apt-get -y -q upgrade gcc make openresty-yajl-dev openresty
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf lua-resty-jsonb_$(LUA_RESTY_JSONB_VER).orig.tar.gz --strip-components=1 -C lua-resty-jsonb
	cd lua-resty-jsonb \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
