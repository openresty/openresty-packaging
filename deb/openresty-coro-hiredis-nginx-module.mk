## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER := 0.0.4
OPENRESTY_VER := 1.21.4.2rc1

.PHONY: openresty-coro-hiredis-nginx-module-download
openresty-coro-hiredis-nginx-module-download:
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-$(OPENRESTY_VER).tar.gz'
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/coro-hiredis-nginx-module-$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER).tar.gz ./
	rm -rf openresty-coro-hiredis-nginx-module_$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER)
	mkdir -p openresty-coro-hiredis-nginx-module_$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER)
	tar -xf openresty-$(OPENRESTY_VER).tar.gz -C openresty-coro-hiredis-nginx-module_$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER)
	tar -xf coro-hiredis-nginx-module-$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER).tar.gz --strip-components=1 -C openresty-coro-hiredis-nginx-module_$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER)
	tar -czf openresty-coro-hiredis-nginx-module_$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER).orig.tar.gz openresty-coro-hiredis-nginx-module_$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER)

openresty-coro-hiredis-nginx-module-clean:
	-cd openresty-coro-hiredis-nginx-module && debclean
	-find openresty-coro-hiredis-nginx-module -maxdepth 1 ! -name 'debian' ! -name 'openresty-coro-hiredis-nginx-module' -print | xargs rm -rf
	rm -rf openresty-coro-hiredis-nginx-module*.deb
	rm -rf openresty-coro-hiredis-nginx-module_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-coro-hiredis-nginx-module-build
openresty-coro-hiredis-nginx-module-build: openresty-coro-hiredis-nginx-module-clean openresty-coro-hiredis-nginx-module-download
	sudo apt-get -y -q install ccache gcc make perl openresty-coro-nginx-module-dev openresty-elf-loader-dev openresty-hiredis-dev openresty openresty-elfutils-dev openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl openresty-coro-nginx-module-dev openresty-elf-loader-dev openresty-hiredis-dev openresty openresty-elfutils-dev openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-coro-hiredis-nginx-module_$(OPENRESTY_CORO_HIREDIS_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C openresty-coro-hiredis-nginx-module
	cd openresty-coro-hiredis-nginx-module \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
