## Author: spec2deb.pl
### Version: 0.01

LUA_RESTY_JSONB_1_17_8_2_VER := 0.0.1

.PHONY: lua-resty-jsonb-1.17.8.2-download
lua-resty-jsonb-1.17.8.2-download:
	rsync -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-resty-jsonb-$(LUA_RESTY_JSONB_1_17_8_2_VER).tar.gz ./
	rm -rf lua-resty-jsonb-1.17.8.2_$(LUA_RESTY_JSONB_1_17_8_2_VER)
	mkdir -p lua-resty-jsonb-1.17.8.2_$(LUA_RESTY_JSONB_1_17_8_2_VER)
	tar -xf lua-resty-jsonb-$(LUA_RESTY_JSONB_1_17_8_2_VER).tar.gz --strip-components=1 -C lua-resty-jsonb-1.17.8.2_$(LUA_RESTY_JSONB_1_17_8_2_VER)
	tar -czf lua-resty-jsonb-1.17.8.2_$(LUA_RESTY_JSONB_1_17_8_2_VER).orig.tar.gz lua-resty-jsonb-1.17.8.2_$(LUA_RESTY_JSONB_1_17_8_2_VER)

lua-resty-jsonb-1.17.8.2-clean:
	cd lua-resty-jsonb-1.17.8.2 && debclean
	-find lua-resty-jsonb-1.17.8.2 -maxdepth 1 ! -name 'debian' ! -name 'lua-resty-jsonb-1.17.8.2' -print | xargs rm -rf
	rm -rf lua-resty-jsonb-1.17.8.2*.deb
	rm -rf lua-resty-jsonb-1.17.8.2_*.*

.PHONY: lua-resty-jsonb-1.17.8.2-build
lua-resty-jsonb-1.17.8.2-build: lua-resty-jsonb-1.17.8.2-clean lua-resty-jsonb-1.17.8.2-download
	sudo apt-get -y -q install gcc make openresty-yajl-dev openresty
	sudo apt-get -y -q upgrade gcc make openresty-yajl-dev openresty
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf lua-resty-jsonb-1.17.8.2_$(LUA_RESTY_JSONB_1_17_8_2_VER).orig.tar.gz --strip-components=1 -C lua-resty-jsonb-1.17.8.2
	cd lua-resty-jsonb-1.17.8.2 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
