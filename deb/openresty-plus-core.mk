## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PLUS_CORE_VER := $(OR_PLUS_VER)

.PHONY: openresty-plus-core-download
openresty-plus-core-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/openresty-plus-$(OPENRESTY_PLUS_CORE_VER).tar.gz ./
	rm -rf openresty-plus-core_$(OPENRESTY_PLUS_CORE_VER)
	mkdir -p openresty-plus-core_$(OPENRESTY_PLUS_CORE_VER)
	tar -xf openresty-plus-$(OPENRESTY_PLUS_CORE_VER).tar.gz --strip-components=1 -C openresty-plus-core_$(OPENRESTY_PLUS_CORE_VER)
	tar -czf openresty-plus-core_$(OPENRESTY_PLUS_CORE_VER).orig.tar.gz openresty-plus-core_$(OPENRESTY_PLUS_CORE_VER)

openresty-plus-core-clean:
	-cd openresty-plus-core && debclean
	-find openresty-plus-core -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-core' -print | xargs rm -rf
	rm -rf openresty-plus-core*.deb
	rm -rf openresty-plus-core/debian/control
	rm -rf openresty-plus-core/debian/rules
	rm -rf openresty-plus-core_*.*

.PHONY: openresty-plus-core-build
openresty-plus-core-build: openresty-plus-core-clean openresty-plus-core-download
ifeq ($(WITH_LUA_LDAP), 1)
	sudo apt-get -y -qq install libldap-2.4-2 libldap-dev
	sudo apt-get -y -qq --only-upgrade install libldap-2.4-2 libldap-dev
endif
ifeq ($(ARCH), amd64)
	sudo apt-get -y -qq install openresty-plus-hyperscan-dev
	sudo apt-get -y -qq --only-upgrade install openresty-plus-hyperscan-dev
endif
ifeq ($(WITH_CORO_NGINX_MODULE), 1)
	sudo apt-get -y -q install openresty-elfutils-dev openresty-elf-loader-dev openresty-libcco-dev openresty-libmariadb-dev openresty-libmemcached-dev openresty-cyrus-sasl-dev openresty-hiredis-dev
	sudo apt-get -y -q install --only-upgrade openresty-elfutils-dev openresty-elf-loader-dev openresty-libcco-dev openresty-libmariadb-dev openresty-libmemcached-dev openresty-cyrus-sasl-dev openresty-hiredis-dev
endif
ifeq ($(WITH_TCMALLOC), 1)
	sudo apt-get -y -q install --no-install-recommends openresty-tcmalloc openresty-tcmalloc-dev
	sudo apt-get -y -q install --only-upgrade openresty-tcmalloc openresty-tcmalloc-dev
endif
	sudo apt-get -y -q install --no-install-recommends ccache make perl valgrind gcc openresty-saas-zlib-dev openresty-plus-openssl111-dev openresty-pcre-dev openresty-yajl-dev libgd-dev libc-dev $(deb_toolchain_pkgs)
	sudo apt-get -y -q install --only-upgrade ccache make perl valgrind gcc openresty-saas-zlib-dev openresty-plus-openssl111-dev openresty-pcre-dev openresty-yajl-dev libgd-dev libc-dev $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-core_$(OPENRESTY_PLUS_CORE_VER).orig.tar.gz --strip-components=1 -C openresty-plus-core
	cd openresty-plus-core \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define with_lua_ldap=$(WITH_LUA_LDAP)  \
			--define with_lua_resty_ldap=$(WITH_LUA_RESTY_LDAP) \
			--define with_lua_resty_openidc=$(WITH_LUA_RESTY_OPENIDC) \
			--define with_lua_resty_session=$(WITH_LUA_RESTY_SESSION) \
			--define with_lua_resty_openssl=$(WITH_LUA_RESTY_OPENSSL) \
			--define with_lua_resty_jwt=$(WITH_LUA_RESTY_JWT) \
			--define with_lua_resty_mlcache=$(WITH_LUA_RESTY_MLCACHE) \
			--define with_ngx_brotli=$(WITH_NGX_BROTLI) \
			--define with_lua_resty_mail=$(WITH_LUA_RESTY_MAIL) \
			--define with_coro_nginx_module=$(WITH_CORO_NGINX_MODULE) \
			--define with_tcmalloc=$(WITH_TCMALLOC) \
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
			--define with_lua_resty_mail=$(WITH_LUA_RESTY_MAIL) \
			--define with_coro_nginx_module=$(WITH_CORO_NGINX_MODULE) \
			--define with_tcmalloc=$(WITH_TCMALLOC) \
			--define arch=$(ARCH) \
			--define with_lua_resty_hmac=$(WITH_LUA_RESTY_HMAC) debian/control.tt2 > debian/control \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
