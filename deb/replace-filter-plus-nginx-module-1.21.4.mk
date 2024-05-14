## Author: spec2deb.pl
### Version: 0.01

REPLACE_FILTER_PLUS_NGINX_MODULE_VER := 0.0.2
NGX_VER := 1.21.4
OPENRESTY_VER := $(NGX_VER).1

.PHONY: replace-filter-plus-nginx-module-1.21.4-download
replace-filter-plus-nginx-module-1.21.4-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/replace-filter-nginx-module-plus-$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER).tar.gz ./
	rm -rf replace-filter-plus-nginx-module-$(NGX_VER)_$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER)
	mkdir -p replace-filter-plus-nginx-module-$(NGX_VER)_$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER)/openresty-$(OPENRESTY_VER)
	tar -xf replace-filter-nginx-module-plus-$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER).tar.gz --strip-components=1 -C replace-filter-plus-nginx-module-$(NGX_VER)_$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER)
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-$(OPENRESTY_VER).tar.gz'
	tar -xf openresty-$(OPENRESTY_VER).tar.gz --strip-components=1 -C replace-filter-plus-nginx-module-$(NGX_VER)_$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER)/openresty-$(OPENRESTY_VER)
	tar -czf replace-filter-plus-nginx-module-$(NGX_VER)_$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER).orig.tar.gz replace-filter-plus-nginx-module-$(NGX_VER)_$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER)

replace-filter-plus-nginx-module-1.21.4-clean:
	-cd replace-filter-plus-nginx-module-$(NGX_VER) && debclean
	-find replace-filter-plus-nginx-module-$(NGX_VER) -maxdepth 1 ! -name 'debian' ! -name 'replace-filter-plus-nginx-module-$(NGX_VER)' -print | xargs rm -rf
	rm -rf replace-filter-plus-nginx-module-$(NGX_VER)*.deb
	rm -rf replace-filter-plus-nginx-module-$(NGX_VER)_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: replace-filter-plus-nginx-module-1.21.4-build
replace-filter-plus-nginx-module-1.21.4-build: replace-filter-plus-nginx-module-1.21.4-clean replace-filter-plus-nginx-module-1.21.4-download
	sudo apt-get -y -q install ccache gcc make perl openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev openresty-perl openresty-perl-b-c openresty-perl-dev openresty-perl-ipc-run3
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev openresty-perl openresty-perl-b-c openresty-perl-dev openresty-perl-ipc-run3
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf replace-filter-plus-nginx-module-$(NGX_VER)_$(REPLACE_FILTER_PLUS_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C replace-filter-plus-nginx-module-$(NGX_VER)
	cd replace-filter-plus-nginx-module-$(NGX_VER) \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
