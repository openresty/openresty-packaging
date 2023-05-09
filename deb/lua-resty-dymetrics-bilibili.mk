## Author: spec2deb.pl
### Version: 0.01

LUA_RESTY_DYMETRICS_BILIBILI_VER := 0.0.3

.PHONY: lua-resty-dymetrics-bilibili-download
lua-resty-dymetrics-bilibili-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-resty-dymetrics-bilibili-$(LUA_RESTY_DYMETRICS_BILIBILI_VER).tar.gz ./
	rm -rf lua-resty-dymetrics-bilibili_$(LUA_RESTY_DYMETRICS_BILIBILI_VER)
	mkdir -p lua-resty-dymetrics-bilibili_$(LUA_RESTY_DYMETRICS_BILIBILI_VER)
	tar -xf lua-resty-dymetrics-bilibili-$(LUA_RESTY_DYMETRICS_BILIBILI_VER).tar.gz --strip-components=1 -C lua-resty-dymetrics-bilibili_$(LUA_RESTY_DYMETRICS_BILIBILI_VER)
	tar -czf lua-resty-dymetrics-bilibili_$(LUA_RESTY_DYMETRICS_BILIBILI_VER).orig.tar.gz lua-resty-dymetrics-bilibili_$(LUA_RESTY_DYMETRICS_BILIBILI_VER)

lua-resty-dymetrics-bilibili-clean:
	-cd lua-resty-dymetrics-bilibili && debclean
	-find lua-resty-dymetrics-bilibili -maxdepth 1 ! -name 'debian' ! -name 'lua-resty-dymetrics-bilibili' -print | xargs rm -rf
	rm -rf lua-resty-dymetrics-bilibili*.deb
	rm -rf lua-resty-dymetrics-bilibili_*.*

.PHONY: lua-resty-dymetrics-bilibili-build
lua-resty-dymetrics-bilibili-build: lua-resty-dymetrics-bilibili-clean lua-resty-dymetrics-bilibili-download
	sudo apt-get -y -q install gcc make openresty-yajl-dev openresty
	sudo apt-get -y -q install --only-upgrade gcc make openresty-yajl-dev openresty
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf lua-resty-dymetrics-bilibili_$(LUA_RESTY_DYMETRICS_BILIBILI_VER).orig.tar.gz --strip-components=1 -C lua-resty-dymetrics-bilibili
	cd lua-resty-dymetrics-bilibili \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
