## Author: spec2deb.pl
### Version: 0.01

#OPENRESTY_PLUS_CORE_H3_VER := $(OR_PLUS_VER)

.PHONY: openresty-plus-core-h3-download
openresty-plus-core-h3-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/openresty-plus-h3-$(OPENRESTY_PLUS_CORE_H3_VER).tar.gz ./
	rm -rf openresty-plus-core-h3_$(OPENRESTY_PLUS_CORE_H3_VER)
	mkdir -p openresty-plus-core-h3_$(OPENRESTY_PLUS_CORE_H3_VER)
	tar -xf openresty-plus-h3-$(OPENRESTY_PLUS_CORE_H3_VER).tar.gz --strip-components=1 -C openresty-plus-core-h3_$(OPENRESTY_PLUS_CORE_H3_VER)
	tar -czf openresty-plus-core-h3_$(OPENRESTY_PLUS_CORE_H3_VER).orig.tar.gz openresty-plus-core-h3_$(OPENRESTY_PLUS_CORE_H3_VER)

openresty-plus-core-h3-clean:
	-cd openresty-plus-core-h3 && debclean
	-find openresty-plus-core-h3 -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-core-h3' -print | xargs rm -rf
	rm -rf openresty-plus-core-h3*.deb
	rm -rf openresty-plus-core-h3_*.*

.PHONY: openresty-plus-core-h3-build
openresty-plus-core-h3-build: openresty-plus-core-h3-clean openresty-plus-core-h3-download
ifeq ($(ARCH), amd64)
	sudo apt-get -y -qq install openresty-plus-hyperscan-dev
	sudo apt-get -y -qq --only-upgrade install openresty-plus-hyperscan-dev
endif
ifeq ($(WITH_CORO_NGINX_MODULE), 1)
	sudo apt-get -y -q install openresty-elfutils-dev openresty-elf-loader-dev openresty-libcco-dev openresty-libmariadb-dev openresty-libmemcached-dev openresty-cyrus-sasl-dev
	sudo apt-get -y -q install --only-upgrade openresty-elfutils-dev openresty-elf-loader-dev openresty-libcco-dev openresty-libmariadb-dev openresty-libmemcached-dev openresty-cyrus-sasl-dev
endif
ifeq ($(WITH_TCMALLOC), 1)
	sudo apt-get -y -q install --no-install-recommends openresty-tcmalloc openresty-tcmalloc-dev
	sudo apt-get -y -q install --only-upgrade openresty-tcmalloc openresty-tcmalloc-dev
endif
	sudo apt-get -y -q install ccache gcc make perl systemtap-sdt-dev openresty-zlib-dev openresty-boringssl-dev openresty-pcre-dev openresty-yajl-dev libtool libgd-dev libc-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl systemtap-sdt-dev openresty-zlib-dev openresty-boringssl-dev openresty-pcre-dev openresty-yajl-dev libtool libgd-dev libc-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-core-h3_$(OPENRESTY_PLUS_CORE_H3_VER).orig.tar.gz --strip-components=1 -C openresty-plus-core-h3
	cd openresty-plus-core-h3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define with_lua_ldap=$(WITH_LUA_LDAP)  \
			--define with_lua_resty_ldap=$(WITH_LUA_RESTY_LDAP) \
			--define with_lua_resty_openidc=$(WITH_LUA_RESTY_OPENIDC) \
			--define with_lua_resty_session=$(WITH_LUA_RESTY_SESSION) \
			--define with_lua_resty_openssl=$(WITH_LUA_RESTY_OPENSSL) \
			--define with_lua_resty_jwt=$(WITH_LUA_RESTY_JWT) \
			--define with_lua_resty_mlcache=$(WITH_LUA_RESTY_MLCACHE) \
			--define with_ngx_brotli=$(WITH_NGX_BROTLI) \
			--define with_lua_resty_hmac=$(WITH_LUA_RESTY_HMAC) \
			--define with_lua_resty_mail=$(WITH_LUA_RESTY_MAIL) \
			--define with_coro_nginx_module=$(WITH_CORO_NGINX_MODULE) \
			--define with_tcmalloc=$(WITH_TCMALLOC) \
			--define arch=$(ARCH) debian/rules.tt2 > debian/rules \
		&& tpage --define with_lua_ldap=$(WITH_LUA_LDAP) \
			--define with_lua_resty_ldap=$(WITH_LUA_RESTY_LDAP) \
			--define with_lua_resty_openidc=$(WITH_LUA_RESTY_OPENIDC) \
			--define with_lua_resty_session=$(WITH_LUA_RESTY_SESSION) \
			--define with_lua_resty_openssl=$(WITH_LUA_RESTY_OPENSSL) \
			--define with_lua_resty_jwt=$(WITH_LUA_RESTY_JWT) \
			--define with_lua_resty_mlcache=$(WITH_LUA_RESTY_MLCACHE) \
			--define with_ngx_brotli=$(WITH_NGX_BROTLI) \
			--define with_lua_resty_hmac=$(WITH_LUA_RESTY_HMAC) \
			--define with_lua_resty_mail=$(WITH_LUA_RESTY_MAIL) \
			--define with_coro_nginx_module=$(WITH_CORO_NGINX_MODULE) \
			--define with_tcmalloc=$(WITH_TCMALLOC) \
			--define arch=$(ARCH) debian/control.tt2 > debian/control \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
