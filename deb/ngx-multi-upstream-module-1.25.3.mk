## Author: spec2deb.pl
### Version: 0.01

NGX_MULTI_UPSTREAM_MODULE_VER := 1.2.0.1

.PHONY: ngx-multi-upstream-module-1.25.3-download
ngx-multi-upstream-module-1.25.3-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/ngx_multi_upstream_module-$(NGX_MULTI_UPSTREAM_MODULE_VER).tar.gz ./
	wget https://openresty.org/download/openresty-1.25.3.1.tar.gz
	wget https://github.com/api7/mod_dubbo/archive/refs/tags/1.0.2.tar.gz
	rm -rf ngx-multi-upstream-module-1.25.3_$(NGX_MULTI_UPSTREAM_MODULE_VER)
	mkdir -p ngx-multi-upstream-module-1.25.3_$(NGX_MULTI_UPSTREAM_MODULE_VER)
	tar -xf ngx_multi_upstream_module-$(NGX_MULTI_UPSTREAM_MODULE_VER).tar.gz --strip-components=1 -C ngx-multi-upstream-module-1.25.3_$(NGX_MULTI_UPSTREAM_MODULE_VER)
	tar -xf openresty-1.25.3.1.tar.gz -C ngx-multi-upstream-module-1.25.3_$(NGX_MULTI_UPSTREAM_MODULE_VER)
	tar -xf 1.0.2.tar.gz -C ngx-multi-upstream-module-1.25.3_$(NGX_MULTI_UPSTREAM_MODULE_VER)
	tar -czf ngx-multi-upstream-module-1.25.3_$(NGX_MULTI_UPSTREAM_MODULE_VER).orig.tar.gz ngx-multi-upstream-module-1.25.3_$(NGX_MULTI_UPSTREAM_MODULE_VER)
	rm openresty-1.25.3.1.tar.gz 1.0.2.tar.gz

ngx-multi-upstream-module-1.25.3-clean:
	-cd ngx-multi-upstream-module-1.25.3 && debclean
	-find ngx-multi-upstream-module-1.25.3 -maxdepth 1 ! -name 'debian' ! -name 'ngx-multi-upstream-module-1.25.3' -print | xargs rm -rf
	rm -rf ngx-multi-upstream-module-1.25.3*.deb
	rm -rf ngx-multi-upstream-module-1.25.3_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: ngx-multi-upstream-module-1.25.3-build
ngx-multi-upstream-module-1.25.3-build: ngx-multi-upstream-module-1.25.3-clean ngx-multi-upstream-module-1.25.3-download
	sudo apt-get -y -q install ccache gcc make perl openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf ngx-multi-upstream-module-1.25.3_$(NGX_MULTI_UPSTREAM_MODULE_VER).orig.tar.gz --strip-components=1 -C ngx-multi-upstream-module-1.25.3
	cd ngx-multi-upstream-module-1.25.3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
