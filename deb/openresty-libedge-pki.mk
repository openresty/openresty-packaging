## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LIBEDGE_PKI_VER := 1.1.5

.PHONY: openresty-libedge-pki-download
openresty-libedge-pki-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/edge-pki-$(OPENRESTY_LIBEDGE_PKI_VER).tar.gz ./
	rm -rf openresty-libedge-pki_$(OPENRESTY_LIBEDGE_PKI_VER)
	mkdir -p openresty-libedge-pki_$(OPENRESTY_LIBEDGE_PKI_VER)
	tar -xf edge-pki-$(OPENRESTY_LIBEDGE_PKI_VER).tar.gz --strip-components=1 -C openresty-libedge-pki_$(OPENRESTY_LIBEDGE_PKI_VER)
	tar -czf openresty-libedge-pki_$(OPENRESTY_LIBEDGE_PKI_VER).orig.tar.gz openresty-libedge-pki_$(OPENRESTY_LIBEDGE_PKI_VER)

openresty-libedge-pki-clean:
	-cd openresty-libedge-pki && debclean
	-find openresty-libedge-pki -maxdepth 1 ! -name 'debian' ! -name 'openresty-libedge-pki' -print | xargs rm -rf
	rm -rf openresty-libedge-pki*.deb
	rm -rf openresty-libedge-pki_*.*

.PHONY: openresty-libedge-pki-build
openresty-libedge-pki-build: openresty-libedge-pki-clean openresty-libedge-pki-download
	sudo apt-get -y -q install gcc make libssl-dev
	sudo apt-get -y -q install --only-upgrade gcc make libssl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-libedge-pki_$(OPENRESTY_LIBEDGE_PKI_VER).orig.tar.gz --strip-components=1 -C openresty-libedge-pki
	cd openresty-libedge-pki \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
