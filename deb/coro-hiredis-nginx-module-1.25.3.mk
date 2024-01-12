## Author: spec2deb.pl
### Version: 0.01

CORO_HIREDIS_NGINX_MODULE_VER := 0.0.5

.PHONY: coro-hiredis-nginx-module-1.25.3-download
coro-hiredis-nginx-module-1.25.3-download:
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-1.25.3.1.tar.gz'
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/coro-hiredis-nginx-module-$(CORO_HIREDIS_NGINX_MODULE_VER).tar.gz ./
	rm -rf coro-hiredis-nginx-module-1.25.3_$(CORO_HIREDIS_NGINX_MODULE_VER)
	mkdir -p coro-hiredis-nginx-module-1.25.3_$(CORO_HIREDIS_NGINX_MODULE_VER)
	tar -xf openresty-1.25.3.1.tar.gz -C coro-hiredis-nginx-module-1.25.3_$(CORO_HIREDIS_NGINX_MODULE_VER)
	tar -xf coro-hiredis-nginx-module-$(CORO_HIREDIS_NGINX_MODULE_VER).tar.gz --strip-components=1 -C coro-hiredis-nginx-module-1.25.3_$(CORO_HIREDIS_NGINX_MODULE_VER)
	tar -czf coro-hiredis-nginx-module-1.25.3_$(CORO_HIREDIS_NGINX_MODULE_VER).orig.tar.gz coro-hiredis-nginx-module-1.25.3_$(CORO_HIREDIS_NGINX_MODULE_VER)

coro-hiredis-nginx-module-1.25.3-clean:
	-cd coro-hiredis-nginx-module-1.25.3 && debclean
	-find coro-hiredis-nginx-module-1.25.3 -maxdepth 1 ! -name 'debian' ! -name 'coro-hiredis-nginx-module-1.25.3' -print | xargs rm -rf
	rm -rf coro-hiredis-nginx-module-1.25.3*.deb
	rm -rf coro-hiredis-nginx-module-1.25.3_*.*
	rm -rf coro-hiredis-nginx-module-1.25.3/debian/changelog

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: coro-hiredis-nginx-module-1.25.3-build
coro-hiredis-nginx-module-1.25.3-build: coro-hiredis-nginx-module-1.25.3-clean coro-hiredis-nginx-module-1.25.3-download
	sudo apt-get -y -q install ccache gcc make perl coro-nginx-module-1.25.3-dev openresty-elf-loader-dev openresty-hiredis-dev openresty openresty-elfutils-dev openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl coro-nginx-module-1.25.3-dev openresty-elf-loader-dev openresty-hiredis-dev openresty-elfutils-dev openresty-zlib-dev openresty-pcre-dev openresty-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf coro-hiredis-nginx-module-1.25.3_$(CORO_HIREDIS_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C coro-hiredis-nginx-module-1.25.3
	cd coro-hiredis-nginx-module-1.25.3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
