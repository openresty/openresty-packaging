## Author: spec2deb.pl
### Version: 0.01

LUA_RESTY_REDIS_CLUSTER_FAST_VER := 0.0.4

.PHONY: lua-resty-redis-cluster-fast-1.25.3-download
lua-resty-redis-cluster-fast-1.25.3-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-resty-redis-cluster-fast-$(LUA_RESTY_REDIS_CLUSTER_FAST_VER).tar.gz ./
	rm -rf lua-resty-redis-cluster-fast-1.25.3_$(LUA_RESTY_REDIS_CLUSTER_FAST_VER)
	mkdir -p lua-resty-redis-cluster-fast-1.25.3_$(LUA_RESTY_REDIS_CLUSTER_FAST_VER)
	tar -xf lua-resty-redis-cluster-fast-$(LUA_RESTY_REDIS_CLUSTER_FAST_VER).tar.gz --strip-components=1 -C lua-resty-redis-cluster-fast-1.25.3_$(LUA_RESTY_REDIS_CLUSTER_FAST_VER)
	tar -czf lua-resty-redis-cluster-fast-1.25.3_$(LUA_RESTY_REDIS_CLUSTER_FAST_VER).orig.tar.gz lua-resty-redis-cluster-fast-1.25.3_$(LUA_RESTY_REDIS_CLUSTER_FAST_VER)

lua-resty-redis-cluster-fast-1.25.3-clean:
	-cd lua-resty-redis-cluster-fast-1.25.3 && debclean
	-find lua-resty-redis-cluster-fast-1.25.3 -maxdepth 1 ! -name 'debian' ! -name 'lua-resty-redis-cluster-fast-1.25.3' -print | xargs rm -rf
	rm -rf lua-resty-redis-cluster-fast-1.25.3*.deb
	rm -rf lua-resty-redis-cluster-fast-1.25.3_*.*
	rm -rf lua-resty-redis-cluster-fast-1.25.3/debian/changelog

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: lua-resty-redis-cluster-fast-1.25.3-build
lua-resty-redis-cluster-fast-1.25.3-build: lua-resty-redis-cluster-fast-1.25.3-clean lua-resty-redis-cluster-fast-1.25.3-download
	sudo apt-get -y -q install openresty
	sudo apt-get -y -q install --only-upgrade openresty
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf lua-resty-redis-cluster-fast-1.25.3_$(LUA_RESTY_REDIS_CLUSTER_FAST_VER).orig.tar.gz --strip-components=1 -C lua-resty-redis-cluster-fast-1.25.3
	cd lua-resty-redis-cluster-fast-1.25.3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
