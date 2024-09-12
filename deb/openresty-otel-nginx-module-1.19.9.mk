## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_OTEL_NGINX_MODULE_VER := 0.1.1.1

.PHONY: openresty-otel-nginx-module-1.19.9-download
openresty-otel-nginx-module-1.19.9-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/nginx-otel-plus-$(OPENRESTY_OTEL_NGINX_MODULE_VER).tar.gz ./
	! test -f openresty-1.19.9.2.tar.gz && wget -O openresty-1.19.9.2.tar.gz https://openresty.org/download/openresty-1.19.9.2.tar.gz || true
	rm -rf openresty-otel-nginx-module-1.19.9_$(OPENRESTY_OTEL_NGINX_MODULE_VER)
	mkdir -p openresty-otel-nginx-module-1.19.9_$(OPENRESTY_OTEL_NGINX_MODULE_VER)
	tar -xf nginx-otel-plus-$(OPENRESTY_OTEL_NGINX_MODULE_VER).tar.gz --strip-components=1 -C openresty-otel-nginx-module-1.19.9_$(OPENRESTY_OTEL_NGINX_MODULE_VER)
	tar -xf openresty-1.19.9.2.tar.gz -C openresty-otel-nginx-module-1.19.9_$(OPENRESTY_OTEL_NGINX_MODULE_VER)
	tar -czf openresty-otel-nginx-module-1.19.9_$(OPENRESTY_OTEL_NGINX_MODULE_VER).orig.tar.gz openresty-otel-nginx-module-1.19.9_$(OPENRESTY_OTEL_NGINX_MODULE_VER)

openresty-otel-nginx-module-1.19.9-clean:
	-cd openresty-otel-nginx-module-1.19.9 && debclean
	-find openresty-otel-nginx-module-1.19.9 -maxdepth 1 ! -name 'debian' ! -name 'openresty-otel-nginx-module-1.19.9' -print | xargs rm -rf
	rm -rf openresty-otel-nginx-module-1.19.9*.deb
	rm -rf openresty-otel-nginx-module-1.19.9_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-otel-nginx-module-1.19.9-build
openresty-otel-nginx-module-1.19.9-build: openresty-otel-nginx-module-1.19.9-clean openresty-otel-nginx-module-1.19.9-download
	sudo apt-get -y -q install ccache gcc cmake make perl libc-ares-dev openresty-plus-openssl111-dev openresty-saas-zlib-dev openresty-pcre-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc cmake make perl libc-ares-dev openresty-plus-openssl111-dev openresty-saas-zlib-dev openresty-pcre-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-otel-nginx-module-1.19.9_$(OPENRESTY_OTEL_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C openresty-otel-nginx-module-1.19.9
	cd openresty-otel-nginx-module-1.19.9 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
