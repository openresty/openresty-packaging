## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_UTILS_VER := 0.28

deb_toolchain_pkgs=debhelper devscripts

.PHONY: openresty-utils-download
openresty-utils-download:
	rsync -av -e \
		"ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" \
		nuc:~/work/openresty-utils-$(OPENRESTY_UTILS_VER).tar.gz ./
	rm -rf openresty-utils_$(OPENRESTY_UTILS_VER)
	mkdir -p openresty-utils_$(OPENRESTY_UTILS_VER)
	tar -xf openresty-utils-$(OPENRESTY_UTILS_VER).tar.gz --strip-components=1 -C openresty-utils_$(OPENRESTY_UTILS_VER)
	tar -czf openresty-utils_$(OPENRESTY_UTILS_VER).orig.tar.gz openresty-utils_$(OPENRESTY_UTILS_VER)

openresty-utils-clean:
	-cd openresty-utils && debclean
	-find openresty-utils -maxdepth 1 ! -name 'debian' ! -name 'openresty-utils' -print | xargs rm -rf
	rm -rf openresty-utils*.deb
	rm -rf openresty-utils_*.*

.PHONY: openresty-utils-build
openresty-utils-build: openresty-utils-clean openresty-utils-download
	sudo apt-get -y -q install ccache gcc make $(deb_toolchain_pkgs) openresty-saas-pcre-dev openresty-saas-pcre2-dev
	sudo apt-get -y -q --only-upgrade install ccache gcc make $(deb_toolchain_pkgs) openresty-saas-pcre-dev openresty-saas-pcre2-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-utils_$(OPENRESTY_UTILS_VER).orig.tar.gz --strip-components=1 -C openresty-utils
	cd openresty-utils \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
