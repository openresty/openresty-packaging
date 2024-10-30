## Author: spec2deb.pl
### Version: 0.01

DYMETRICS_NGINX_MODULE_VER := 0.0.19

.PHONY: dymetrics-nginx-module-1.25.3-download
dymetrics-nginx-module-1.25.3-download:
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-1.25.3.2.tar.gz'
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-resty-dymetrics-$(DYMETRICS_NGINX_MODULE_VER).tar.gz ./
	rm -rf dymetrics-nginx-module-1.25.3_$(DYMETRICS_NGINX_MODULE_VER)
	mkdir -p dymetrics-nginx-module-1.25.3_$(DYMETRICS_NGINX_MODULE_VER)
	tar -xf openresty-1.25.3.2.tar.gz -C dymetrics-nginx-module-1.25.3_$(DYMETRICS_NGINX_MODULE_VER)
	tar -xf lua-resty-dymetrics-$(DYMETRICS_NGINX_MODULE_VER).tar.gz --strip-components=1 -C dymetrics-nginx-module-1.25.3_$(DYMETRICS_NGINX_MODULE_VER)
	tar -czf dymetrics-nginx-module-1.25.3_$(DYMETRICS_NGINX_MODULE_VER).orig.tar.gz dymetrics-nginx-module-1.25.3_$(DYMETRICS_NGINX_MODULE_VER)

dymetrics-nginx-module-1.25.3-clean:
	-cd dymetrics-nginx-module-1.25.3 && debclean
	-find dymetrics-nginx-module-1.25.3 -maxdepth 1 ! -name 'debian' ! -name 'dymetrics-nginx-module-1.25.3' -print | xargs rm -rf
	rm -rf dymetrics-nginx-module-1.25.3*.deb
	rm -rf dymetrics-nginx-module-1.25.3_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: dymetrics-nginx-module-1.25.3-build
dymetrics-nginx-module-1.25.3-build: dymetrics-nginx-module-1.25.3-clean dymetrics-nginx-module-1.25.3-download
	sudo apt-get -y -q install ccache gcc make perl openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev
	sudo apt-get -y -q install --only-upgrade ccache gcc make perl openresty-openssl111-dev openresty-zlib-dev openresty-pcre-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf dymetrics-nginx-module-1.25.3_$(DYMETRICS_NGINX_MODULE_VER).orig.tar.gz --strip-components=1 -C dymetrics-nginx-module-1.25.3
	cd dymetrics-nginx-module-1.25.3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
