## Author: spec2deb.pl
### Version: 0.01

CORO_LIBCURL_NGINX_MODULE_VER := 0.0.7

.PHONY: coro-libcurl-nginx-module-1.27.1-download
coro-libcurl-nginx-module-1.27.1-download:
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-1.27.1.1.tar.gz'
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/coro-libcurl-nginx-module-$(CORO_LIBCURL_NGINX_MODULE_VER).tar.gz ./
	rm -rf coro-libcurl-nginx-module-1.27.1_$(CORO_LIBCURL_NGINX_MODULE_VER)
	mkdir -p coro-libcurl-nginx-module-1.27.1_$(CORO_LIBCURL_NGINX_MODULE_VER)
	tar -xf openresty-1.27.1.1.tar.gz -C coro-libcurl-nginx-module-1.27.1_$(CORO_LIBCURL_NGINX_MODULE_VER)
	tar -xf coro-libcurl-nginx-module-$(CORO_LIBCURL_NGINX_MODULE_VER).tar.gz --strip-components=1 -C coro-libcurl-nginx-module-1.27.1_$(CORO_LIBCURL_NGINX_MODULE_VER)
	tar -czf coro-libcurl-nginx-module-1.27.1_$(CORO_LIBCURL_NGINX_MODULE_VER).orig.tar.gz coro-libcurl-nginx-module-1.27.1_$(CORO_LIBCURL_NGINX_MODULE_VER)

coro-libcurl-nginx-module-1.27.1-clean:
	-cd coro-libcurl-nginx-module-1.27.1 && debclean
	-find coro-libcurl-nginx-module-1.27.1 -maxdepth 1 ! -name 'debian' ! -name 'coro-libcurl-nginx-module-1.27.1' -print | xargs rm -rf
	rm -rf coro-libcurl-nginx-module-1.27.1*.deb
	rm -rf coro-libcurl-nginx-module-1.27.1_*.*
	rm -rf coro-libcurl-nginx-module-1.27.1/debian/changelog

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: coro-libcurl-nginx-module-1.27.1-build
coro-libcurl-nginx-module-1.27.1-build: coro-libcurl-nginx-module-1.27.1-clean coro-libcurl-nginx-module-1.27.1-download
	sudo apt-get -y -q install ccache gcc make perl coro-nginx-module-1.27.1-dev openresty-elf-loader-dev openresty-libcurl-dev openresty-elfutils-dev openresty-zlib-dev openresty openresty-pcre-dev openresty-openssl111-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl coro-nginx-module-1.27.1-dev openresty-elf-loader-dev openresty-libcurl-dev openresty-elfutils-dev openresty openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf coro-libcurl-nginx-module-1.27.1_$(CORO_LIBCURL_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C coro-libcurl-nginx-module-1.27.1
	cd coro-libcurl-nginx-module-1.27.1 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
