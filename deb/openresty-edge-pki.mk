## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_EDGE_PKI(?:w+)VER := 1.1.8

.PHONY: openresty-edge-pki-download
openresty-edge-pki-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/edge-pki-$(OPENRESTY_EDGE_PKI_VER).tar.gz ./
	rm -rf openresty-edge-pki_$(OPENRESTY_EDGE_PKI_VER)
	mkdir -p openresty-edge-pki_$(OPENRESTY_EDGE_PKI_VER)
	tar -xf edge-pki-$(OPENRESTY_EDGE_PKI_VER).tar.gz --strip-components=1 -C openresty-edge-pki_$(OPENRESTY_EDGE_PKI_VER)
	tar -czf openresty-edge-pki_$(OPENRESTY_EDGE_PKI_VER).orig.tar.gz openresty-edge-pki_$(OPENRESTY_EDGE_PKI_VER)

openresty-edge-pki-clean:
	-cd openresty-edge-pki && debclean
	-find openresty-edge-pki -maxdepth 1 ! -name 'debian' ! -name 'openresty-edge-pki' -print | xargs rm -rf
	rm -rf openresty-edge-pki*.deb
	rm -rf openresty-edge-pki_*.*

.PHONY: openresty-edge-pki-build
openresty-edge-pki-build: openresty-edge-pki-clean openresty-edge-pki-download
	sudo apt-get -y -q install gcc make openresty-plus-core openresty-plus-openssl111-dev
	sudo apt-get -y -q install --only-upgrade gcc make openresty-plus-core openresty-plus-openssl111-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-edge-pki_$(OPENRESTY_EDGE_PKI_VER).orig.tar.gz --strip-components=1 -C openresty-edge-pki
	cd openresty-edge-pki \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
