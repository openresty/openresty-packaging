## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_OTEL_NGINX_MODULE_VER := 0.1.1.1

.PHONY: openresty-otel-nginx-module-NGINX_VERSION-download
openresty-otel-nginx-module-NGINX_VERSION-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/nginx-otel-plus-$(OPENRESTY_OTEL_NGINX_MODULE_VER).tar.gz ./
	! test -f openresty-OPENRESTY_VERSION.tar.gz && wget -O openresty-OPENRESTY_VERSION.tar.gz https://openresty.org/download/openresty-OPENRESTY_VERSION.tar.gz || true
	rm -rf openresty-otel-nginx-module-NGINX_VERSION_$(OPENRESTY_OTEL_NGINX_MODULE_VER)
	mkdir -p openresty-otel-nginx-module-NGINX_VERSION_$(OPENRESTY_OTEL_NGINX_MODULE_VER)
	tar -xf nginx-otel-plus-$(OPENRESTY_OTEL_NGINX_MODULE_VER).tar.gz --strip-components=1 -C openresty-otel-nginx-module-NGINX_VERSION_$(OPENRESTY_OTEL_NGINX_MODULE_VER)
	tar -xf openresty-OPENRESTY_VERSION.tar.gz -C openresty-otel-nginx-module-NGINX_VERSION_$(OPENRESTY_OTEL_NGINX_MODULE_VER)
	tar -czf openresty-otel-nginx-module-NGINX_VERSION_$(OPENRESTY_OTEL_NGINX_MODULE_VER).orig.tar.gz openresty-otel-nginx-module-NGINX_VERSION_$(OPENRESTY_OTEL_NGINX_MODULE_VER)

openresty-otel-nginx-module-NGINX_VERSION-clean:
	-cd openresty-otel-nginx-module-NGINX_VERSION && debclean
	-find openresty-otel-nginx-module-NGINX_VERSION -maxdepth 1 ! -name 'debian' ! -name 'openresty-otel-nginx-module-NGINX_VERSION' -print | xargs rm -rf
	rm -rf openresty-otel-nginx-module-NGINX_VERSION*.deb
	rm -rf openresty-otel-nginx-module-NGINX_VERSION_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-otel-nginx-module-NGINX_VERSION-build
openresty-otel-nginx-module-NGINX_VERSION-build: openresty-otel-nginx-module-NGINX_VERSION-clean openresty-otel-nginx-module-NGINX_VERSION-download
	sudo apt-get -y -q install ccache gcc cmake make perl libc-ares-dev openresty-plus-openssl111-dev openresty-saas-zlib-dev openresty-pcre-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc cmake make perl libc-ares-dev openresty-plus-openssl111-dev openresty-saas-zlib-dev openresty-pcre-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-otel-nginx-module-NGINX_VERSION_$(OPENRESTY_OTEL_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C openresty-otel-nginx-module-NGINX_VERSION
	cd openresty-otel-nginx-module-NGINX_VERSION \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
