## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_UTIL_LINUX_VER := 2.35.1.1

.PHONY: openresty-util-linux-download
openresty-util-linux-download:
	rsync -av -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/util-linux-$(OPENRESTY_UTIL_LINUX_VER).tar.gz .
	rm -rf openresty-util-linux_$(OPENRESTY_UTIL_LINUX_VER)
	mkdir -p openresty-util-linux_$(OPENRESTY_UTIL_LINUX_VER)
	tar -xf util-linux-$(OPENRESTY_UTIL_LINUX_VER).tar.gz --strip-components=1 -C openresty-util-linux_$(OPENRESTY_UTIL_LINUX_VER)
	tar -czf openresty-util-linux_$(OPENRESTY_UTIL_LINUX_VER).orig.tar.gz openresty-util-linux_$(OPENRESTY_UTIL_LINUX_VER)

openresty-util-linux-clean:
	cd openresty-util-linux && debclean
	-find openresty-util-linux -maxdepth 1 ! -name 'debian' ! -name 'openresty-util-linux' -print | xargs rm -rf
	rm -rf openresty-util-linux*.deb
	rm -rf openresty-util-linux_*.*

.PHONY: openresty-util-linux-build
openresty-util-linux-build: openresty-util-linux-clean openresty-util-linux-download
	sudo apt-get -y -q install gettext libselinux-dev ncurses-dev pkg-config
	rm -f *.deb *.debian.tar.gz *.dsc *.changes
	tar xf openresty-util-linux_$(OPENRESTY_UTIL_LINUX_VER).orig.tar.gz --strip-components=1 -C openresty-util-linux
	cd openresty-util-linux \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
