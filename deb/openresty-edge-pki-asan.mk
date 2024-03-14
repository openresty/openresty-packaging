## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_EDGE_PKI_ASAN_VER := 1.1.9

.PHONY: openresty-edge-pki-asan-download
openresty-edge-pki-asan-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/edge-pki-$(OPENRESTY_EDGE_PKI_ASAN_VER).tar.gz ./
	rm -rf openresty-edge-pki-asan_$(OPENRESTY_EDGE_PKI_ASAN_VER)
	mkdir -p openresty-edge-pki-asan_$(OPENRESTY_EDGE_PKI_ASAN_VER)
	tar -xf edge-pki-$(OPENRESTY_EDGE_PKI_ASAN_VER).tar.gz --strip-components=1 -C openresty-edge-pki-asan_$(OPENRESTY_EDGE_PKI_ASAN_VER)
	tar -czf openresty-edge-pki-asan_$(OPENRESTY_EDGE_PKI_ASAN_VER).orig.tar.gz openresty-edge-pki-asan_$(OPENRESTY_EDGE_PKI_ASAN_VER)

openresty-edge-pki-asan-clean:
	-cd openresty-edge-pki-asan && debclean
	-find openresty-edge-pki-asan -maxdepth 1 ! -name 'debian' ! -name 'openresty-edge-pki-asan' -print | xargs rm -rf
	rm -rf openresty-edge-pki-asan*.deb
	rm -rf openresty-edge-pki-asan_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-edge-pki-asan-build
openresty-edge-pki-asan-build: openresty-edge-pki-asan-clean openresty-edge-pki-asan-download
	sudo apt-get -y -q install gcc make openresty-plus-core openresty-plus-openssl111-asan-dev
	sudo apt-get -y -q install --only-upgrade gcc make openresty-plus-core openresty-plus-openssl111-asan-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-edge-pki-asan_$(OPENRESTY_EDGE_PKI_ASAN_VER).orig.tar.gz --strip-components=1 -C openresty-edge-pki-asan
	cd openresty-edge-pki-asan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
