## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_CORO_NGINX_MODULE_VER := 0.0.1
OPENRESTY_VER := 1.21.4.2rc1

.PHONY: openresty-coro-nginx-module-download
openresty-coro-nginx-module-download:
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-$(OPENRESTY_VER).tar.gz'
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/coro-nginx-module-$(OPENRESTY_CORO_NGINX_MODULE_VER).tar.gz ./
	rm -rf openresty-coro-nginx-module_$(OPENRESTY_CORO_NGINX_MODULE_VER)
	mkdir -p openresty-coro-nginx-module_$(OPENRESTY_CORO_NGINX_MODULE_VER)
	tar -xf openresty-$(OPENRESTY_VER).tar.gz -C openresty-coro-nginx-module_$(OPENRESTY_CORO_NGINX_MODULE_VER)
	tar -xf coro-nginx-module-$(OPENRESTY_CORO_NGINX_MODULE_VER).tar.gz --strip-components=1 -C openresty-coro-nginx-module_$(OPENRESTY_CORO_NGINX_MODULE_VER)
	tar -czf openresty-coro-nginx-module_$(OPENRESTY_CORO_NGINX_MODULE_VER).orig.tar.gz openresty-coro-nginx-module_$(OPENRESTY_CORO_NGINX_MODULE_VER)

openresty-coro-nginx-module-clean:
	-cd openresty-coro-nginx-module && debclean
	-find openresty-coro-nginx-module -maxdepth 1 ! -name 'debian' ! -name 'openresty-coro-nginx-module' -print | xargs rm -rf
	rm -rf openresty-coro-nginx-module*.deb
	rm -rf openresty-coro-nginx-module_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-coro-nginx-module-build
openresty-coro-nginx-module-build: openresty-coro-nginx-module-clean openresty-coro-nginx-module-download
	sudo apt-get -y -q install ccache gcc make perl openresty-elf-loader-dev openresty-libcco-dev openresty-elfutils-dev openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl openresty-elf-loader-dev openresty-libcco-dev openresty-elfutils-dev openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-coro-nginx-module_$(OPENRESTY_CORO_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C openresty-coro-nginx-module
	cd openresty-coro-nginx-module \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
