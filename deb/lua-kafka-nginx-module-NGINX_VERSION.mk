## Author: spec2deb.pl
### Version: 0.01

LUA_KAFKA_NGINX_MODULE_VER := 0.0.1

.PHONY: lua-kafka-nginx-module-NGINX_VERSION-download
lua-kafka-nginx-module-NGINX_VERSION-download:
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-OPENRESTY_VERSION.tar.gz'
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-kafka-nginx-module-$(LUA_KAFKA_NGINX_MODULE_VER).tar.gz ./
	rm -rf lua-kafka-nginx-module-NGINX_VERSION_$(LUA_KAFKA_NGINX_MODULE_VER)
	mkdir -p lua-kafka-nginx-module-NGINX_VERSION_$(LUA_KAFKA_NGINX_MODULE_VER)
	tar -xf openresty-OPENRESTY_VERSION.tar.gz -C lua-kafka-nginx-module-NGINX_VERSION_$(LUA_KAFKA_NGINX_MODULE_VER)
	tar -xf lua-kafka-nginx-module-$(LUA_KAFKA_NGINX_MODULE_VER).tar.gz --strip-components=1 -C lua-kafka-nginx-module-NGINX_VERSION_$(LUA_KAFKA_NGINX_MODULE_VER)
	tar -czf lua-kafka-nginx-module-NGINX_VERSION_$(LUA_KAFKA_NGINX_MODULE_VER).orig.tar.gz lua-kafka-nginx-module-NGINX_VERSION_$(LUA_KAFKA_NGINX_MODULE_VER)

lua-kafka-nginx-module-NGINX_VERSION-clean:
	-cd lua-kafka-nginx-module-NGINX_VERSION && debclean
	-find lua-kafka-nginx-module-NGINX_VERSION -maxdepth 1 ! -name 'debian' ! -name 'lua-kafka-nginx-module-NGINX_VERSION' -print | xargs rm -rf
	rm -rf lua-kafka-nginx-module-NGINX_VERSION*.deb
	rm -rf lua-kafka-nginx-module-NGINX_VERSION_*.*
	rm -rf lua-kafka-nginx-module-NGINX_VERSION/debian/changelog

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: lua-kafka-nginx-module-NGINX_VERSION-build
lua-kafka-nginx-module-NGINX_VERSION-build: lua-kafka-nginx-module-NGINX_VERSION-clean lua-kafka-nginx-module-NGINX_VERSION-download
	sudo apt-get -y -q install openresty ccache gcc make openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev openresty-librdkafka-dev openresty-cyrus-sasl-dev openresty-ljsb-dev
	sudo apt-get -y -q install --only-upgrade openresty ccache gcc make openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev openresty-librdkafka-dev openresty-cyrus-sasl-dev openresty-ljsb-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf lua-kafka-nginx-module-NGINX_VERSION_$(LUA_KAFKA_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C lua-kafka-nginx-module-NGINX_VERSION
	cd lua-kafka-nginx-module-NGINX_VERSION \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
