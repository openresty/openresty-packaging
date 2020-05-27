## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_SAAS_VER := 1.15.8.2.8

deb_toolchain_pkgs=debhelper devscripts

.PHONY: openresty-saas-download
openresty-saas-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/openresty-plus-$(OPENRESTY_SAAS_VER).tar.gz ./
	rm -rf openresty-saas_$(OPENRESTY_SAAS_VER)
	mkdir -p openresty-saas_$(OPENRESTY_SAAS_VER)
	tar -xf openresty-plus-$(OPENRESTY_SAAS_VER).tar.gz --strip-components=1 -C openresty-saas_$(OPENRESTY_SAAS_VER)
	tar -czf openresty-saas_$(OPENRESTY_SAAS_VER).orig.tar.gz openresty-saas_$(OPENRESTY_SAAS_VER)

openresty-saas-clean:
	cd openresty-saas && debclean
	-find openresty-saas -maxdepth 1 ! -name 'debian' ! -name 'openresty-saas' -print | xargs rm -rf
	rm -rf openresty-saas*.deb
	rm -rf openresty-saas_*.*

.PHONY: openresty-saas-build
openresty-saas-build: openresty-saas-clean openresty-saas-download
	sudo apt-get -y -q install ccache gcc make perl openresty-saas-zlib-dev openresty-saas-openssl-dev openresty-saas-pcre-dev libgd-dev libc-dev texinfo $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-saas_$(OPENRESTY_SAAS_VER).orig.tar.gz --strip-components=1 -C openresty-saas
	cd openresty-saas \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
