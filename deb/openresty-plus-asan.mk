## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PLUS_ASAN_VER := $(OR_PLUS_VER)

.PHONY: openresty-plus-asan-download
openresty-plus-asan-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/openresty-plus-$(OPENRESTY_PLUS_ASAN_VER).tar.gz ./
	rm -rf openresty-plus-asan_$(OPENRESTY_PLUS_ASAN_VER)
	mkdir -p openresty-plus-asan_$(OPENRESTY_PLUS_ASAN_VER)
	tar -xf openresty-plus-$(OPENRESTY_PLUS_ASAN_VER).tar.gz --strip-components=1 -C openresty-plus-asan_$(OPENRESTY_PLUS_ASAN_VER)
	tar -czf openresty-plus-asan_$(OPENRESTY_PLUS_ASAN_VER).orig.tar.gz openresty-plus-asan_$(OPENRESTY_PLUS_ASAN_VER)

openresty-plus-asan-clean:
	-cd openresty-plus-asan && debclean
	-find openresty-plus-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-asan' -print | xargs rm -rf
	rm -rf openresty-plus-asan*.deb
	rm -rf openresty-plus-asan/debian/control
	rm -rf openresty-plus-asan/debian/rules
	rm -rf openresty-plus-asan_*.*

.PHONY: openresty-plus-asan-build
openresty-plus-asan-build: openresty-plus-asan-clean openresty-plus-asan-download
ifeq ($(WITH_LUA_LDAP), 1)
	sudo apt-get -y -qq install libldap-2.4-2 libldap-dev
	sudo apt-get -y -qq --only-upgrade install libldap-2.4-2 libldap-dev
endif
ifeq ($(ARCH), amd64)
	sudo apt-get -y -qq install openresty-plus-hyperscan-dev
	sudo apt-get -y -qq --only-upgrade install openresty-plus-hyperscan-dev
endif
	sudo apt-get -y -q install ccache make perl valgrind gcc openresty-zlib-asan-dev openresty-plus-openssl111-asan-dev openresty-pcre-asan-dev openresty-yajl-dev libgd-dev libc-dev $(deb_toolchain_pkgs)
	sudo apt-get -y -q install --only-upgrade ccache make perl valgrind gcc openresty-zlib-asan-dev openresty-plus-openssl111-asan-dev openresty-pcre-asan-dev openresty-yajl-dev libgd-dev libc-dev $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-asan_$(OPENRESTY_PLUS_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-plus-asan
	cd openresty-plus-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define with_lua_ldap=$(WITH_LUA_LDAP)  \
			--define with_lua_resty_ldap=$(WITH_LUA_RESTY_LDAP) \
			--define with_lua_resty_openidc=$(WITH_LUA_RESTY_OPENIDC) \
			--define with_lua_resty_session=$(WITH_LUA_RESTY_SESSION) \
			--define with_lua_resty_openssl=$(WITH_LUA_RESTY_OPENSSL) \
			--define with_lua_resty_jwt=$(WITH_LUA_RESTY_JWT) \
			--define with_lua_resty_mlcache=$(WITH_LUA_RESTY_MLCACHE) \
			--define with_ngx_brotli=$(WITH_NGX_BROTLI) \
			--define arch=$(ARCH) \
			--define with_lua_resty_hmac=$(WITH_LUA_RESTY_HMAC) debian/rules.tt2 > debian/rules \
		&& tpage --define with_lua_ldap=$(WITH_LUA_LDAP) \
			--define with_lua_resty_ldap=$(WITH_LUA_RESTY_LDAP) \
			--define with_lua_resty_openidc=$(WITH_LUA_RESTY_OPENIDC) \
			--define with_lua_resty_session=$(WITH_LUA_RESTY_SESSION) \
			--define with_lua_resty_openssl=$(WITH_LUA_RESTY_OPENSSL) \
			--define with_lua_resty_jwt=$(WITH_LUA_RESTY_JWT) \
			--define with_lua_resty_mlcache=$(WITH_LUA_RESTY_MLCACHE) \
			--define with_ngx_brotli=$(WITH_NGX_BROTLI) \
			--define arch=$(ARCH) \
			--define with_lua_resty_hmac=$(WITH_LUA_RESTY_HMAC) debian/control.tt2 > debian/control \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
