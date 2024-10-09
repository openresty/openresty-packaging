## Author: spec2deb.pl
### Version: 0.01

LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER := 1.0.19

.PHONY: lua-resty-limit-traffic-dynamic-download
lua-resty-limit-traffic-dynamic-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-resty-limit-traffic-dynamic-$(LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER).tar.gz ./
	rm -rf lua-resty-limit-traffic-dynamic_$(LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER)
	mkdir -p lua-resty-limit-traffic-dynamic_$(LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER)
	tar -xf lua-resty-limit-traffic-dynamic-$(LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER).tar.gz --strip-components=1 -C lua-resty-limit-traffic-dynamic_$(LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER)
	tar -czf lua-resty-limit-traffic-dynamic_$(LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER).orig.tar.gz lua-resty-limit-traffic-dynamic_$(LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER)

lua-resty-limit-traffic-dynamic-clean:
	-cd lua-resty-limit-traffic-dynamic && debclean
	-find lua-resty-limit-traffic-dynamic -maxdepth 1 ! -name 'debian' ! -name 'lua-resty-limit-traffic-dynamic' -print | xargs rm -rf
	rm -rf lua-resty-limit-traffic-dynamic*.deb
	rm -rf lua-resty-limit-traffic-dynamic_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: lua-resty-limit-traffic-dynamic-build
lua-resty-limit-traffic-dynamic-build: lua-resty-limit-traffic-dynamic-clean lua-resty-limit-traffic-dynamic-download
	sudo apt-get -y -q install openresty ccache gcc make
	sudo apt-get -y -q install --only-upgrade openresty ccache gcc make
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf lua-resty-limit-traffic-dynamic_$(LUA_RESTY_LIMIT_TRAFFIC_DYNAMIC_VER).orig.tar.gz --strip-components=1 -C lua-resty-limit-traffic-dynamic
	cd lua-resty-limit-traffic-dynamic \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
