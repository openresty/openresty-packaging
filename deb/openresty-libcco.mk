## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBCCO_VER := 0.0.1

.PHONY: openresty-libcco-download
openresty-libcco-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/libcco-$(OPENRESTY_LIBCCO_VER).tar.gz ./
	rm -rf openresty-libcco_$(OPENRESTY_LIBCCO_VER)
	mkdir -p openresty-libcco_$(OPENRESTY_LIBCCO_VER)
	tar -xf libcco-$(OPENRESTY_LIBCCO_VER).tar.gz --strip-components=1 -C openresty-libcco_$(OPENRESTY_LIBCCO_VER)
	tar -czf openresty-libcco_$(OPENRESTY_LIBCCO_VER).orig.tar.gz openresty-libcco_$(OPENRESTY_LIBCCO_VER)

openresty-libcco-clean:
	-cd openresty-libcco && debclean
	-find openresty-libcco -maxdepth 1 ! -name 'debian' ! -name 'openresty-libcco' -print | xargs rm -rf
	rm -rf openresty-libcco*.deb
	rm -rf openresty-libcco_*.*

.PHONY: openresty-libcco-build
openresty-libcco-build: openresty-libcco-clean openresty-libcco-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libcco_$(OPENRESTY_LIBCCO_VER).orig.tar.gz --strip-components=1 -C openresty-libcco
	cd openresty-libcco \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
