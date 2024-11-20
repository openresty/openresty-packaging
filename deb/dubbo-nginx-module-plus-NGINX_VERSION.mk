## Author: spec2deb.pl
### Version: 0.01

MOD_DUBBO_VER := 1.0.2.1
NGX_MULTI_UPSTREAM_MODULE_VER := 1.2.0.1

.PHONY: dubbo-nginx-module-plus-NGINX_VERSION-download
dubbo-nginx-module-plus-NGINX_VERSION-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/ngx_multi_upstream_module-$(MOD_DUBBO_VER).tar.gz ./
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/mod_dubbo-$(MOD_DUBBO_VER).tar.gz ./
	wget https://openresty.org/download/openresty-OPENRESTY_VERSION.tar.gz
	rm -rf dubbo-nginx-module-plus-NGINX_VERSION_$(MOD_DUBBO_VER)
	mkdir -p dubbo-nginx-module-plus-NGINX_VERSION_$(MOD_DUBBO_VER)
	tar -xf mod_dubbo-$(MOD_DUBBO_VER).tar.gz --strip-components=1 -C dubbo-nginx-module-plus-NGINX_VERSION_$(MOD_DUBBO_VER)
	tar -xf openresty-OPENRESTY_VERSION.tar.gz -C dubbo-nginx-module-plus-NGINX_VERSION_$(MOD_DUBBO_VER)
	tar -xf ngx_multi_upstream_module-$(NGX_MULTI_UPSTREAM_MODULE_VER).tar.gz -C dubbo-nginx-module-plus-NGINX_VERSION_$(MOD_DUBBO_VER)
	tar -czf dubbo-nginx-module-plus-NGINX_VERSION_$(MOD_DUBBO_VER).orig.tar.gz dubbo-nginx-module-plus-NGINX_VERSION_$(MOD_DUBBO_VER)
	rm openresty-OPENRESTY_VERSION.tar.gz

dubbo-nginx-module-plus-NGINX_VERSION-clean:
	-cd dubbo-nginx-module-plus-NGINX_VERSION && debclean
	-find dubbo-nginx-module-plus-NGINX_VERSION -maxdepth 1 ! -name 'debian' ! -name 'dubbo-nginx-module-plus-NGINX_VERSION' -print | xargs rm -rf
	rm -rf dubbo-nginx-module-plus-NGINX_VERSION*.deb
	rm -rf dubbo-nginx-module-plus-NGINX_VERSION_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: dubbo-nginx-module-plus-NGINX_VERSION-build
dubbo-nginx-module-plus-NGINX_VERSION-build: dubbo-nginx-module-plus-NGINX_VERSION-clean dubbo-nginx-module-plus-NGINX_VERSION-download
	sudo apt-get -y -q install ccache gcc make perl openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf dubbo-nginx-module-plus-NGINX_VERSION_$(MOD_DUBBO_VER).orig.tar.gz --strip-components=1 -C dubbo-nginx-module-plus-NGINX_VERSION
	cd dubbo-nginx-module-plus-NGINX_VERSION \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
