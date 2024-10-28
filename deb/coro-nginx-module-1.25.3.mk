## Author: spec2deb.pl
### Version: 0.01

CORO_NGINX_MODULE_VER := 0.0.13

.PHONY: coro-nginx-module-1.25.3-download
coro-nginx-module-1.25.3-download:
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-1.25.3.1.tar.gz'
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/coro-nginx-module-$(CORO_NGINX_MODULE_VER).tar.gz ./
	rm -rf coro-nginx-module-1.25.3_$(CORO_NGINX_MODULE_VER)
	mkdir -p coro-nginx-module-1.25.3_$(CORO_NGINX_MODULE_VER)
	tar -xf openresty-1.25.3.1.tar.gz -C coro-nginx-module-1.25.3_$(CORO_NGINX_MODULE_VER)
	tar -xf coro-nginx-module-$(CORO_NGINX_MODULE_VER).tar.gz --strip-components=1 -C coro-nginx-module-1.25.3_$(CORO_NGINX_MODULE_VER)
	tar -czf coro-nginx-module-1.25.3_$(CORO_NGINX_MODULE_VER).orig.tar.gz coro-nginx-module-1.25.3_$(CORO_NGINX_MODULE_VER)

coro-nginx-module-1.25.3-clean:
	-cd coro-nginx-module-1.25.3 && debclean
	-find coro-nginx-module-1.25.3 -maxdepth 1 ! -name 'debian' ! -name 'coro-nginx-module-1.25.3' -print | xargs rm -rf
	rm -rf coro-nginx-module-1.25.3*.deb
	rm -rf coro-nginx-module-1.25.3_*.*
	rm -rf coro-nginx-module-1.25.3/debian/changelog

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: coro-nginx-module-1.25.3-build
coro-nginx-module-1.25.3-build: coro-nginx-module-1.25.3-clean coro-nginx-module-1.25.3-download
	sudo apt-get -y -q install ccache gcc make perl openresty-elf-loader-dev openresty-libcco-dev openresty-elfutils-dev openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl openresty-elf-loader-dev openresty-libcco-dev openresty-elfutils-dev openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf coro-nginx-module-1.25.3_$(CORO_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C coro-nginx-module-1.25.3
	cd coro-nginx-module-1.25.3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
