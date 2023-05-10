## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_EBPF_PLUS_VER := 0.0.1

.PHONY: openresty-ebpf-plus-download
openresty-ebpf-plus-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/ebpf-plus-$(OPENRESTY_EBPF_PLUS_VER).tar.gz ./
	rm -rf openresty-ebpf-plus_$(OPENRESTY_EBPF_PLUS_VER)
	mkdir -p openresty-ebpf-plus_$(OPENRESTY_EBPF_PLUS_VER)
	tar -xf ebpf-plus-$(OPENRESTY_EBPF_PLUS_VER).tar.gz --strip-components=1 -C openresty-ebpf-plus_$(OPENRESTY_EBPF_PLUS_VER)
	tar -czf openresty-ebpf-plus_$(OPENRESTY_EBPF_PLUS_VER).orig.tar.gz openresty-ebpf-plus_$(OPENRESTY_EBPF_PLUS_VER)

openresty-ebpf-plus-clean:
	-cd openresty-ebpf-plus && debclean
	-find openresty-ebpf-plus -maxdepth 1 ! -name 'debian' ! -name 'openresty-ebpf-plus' -print | xargs rm -rf
	rm -rf openresty-ebpf-plus*.deb
	rm -rf openresty-ebpf-plus_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-ebpf-plus-build
openresty-ebpf-plus-build: openresty-ebpf-plus-clean openresty-ebpf-plus-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-ebpf-plus_$(OPENRESTY_EBPF_PLUS_VER).orig.tar.gz --strip-components=1 -C openresty-ebpf-plus
	cd openresty-ebpf-plus \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
