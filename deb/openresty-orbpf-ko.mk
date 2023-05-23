## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ORBPF_KO_VER := 0.0.1

.PHONY: openresty-orbpf-ko-download
openresty-orbpf-ko-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/orbpf-ko-$(OPENRESTY_ORBPF_KO_VER).tar.gz ./
	rm -rf openresty-orbpf-ko_$(OPENRESTY_ORBPF_KO_VER)
	mkdir -p openresty-orbpf-ko_$(OPENRESTY_ORBPF_KO_VER)
	tar -xf orbpf-ko-$(OPENRESTY_ORBPF_KO_VER).tar.gz --strip-components=1 -C openresty-orbpf-ko_$(OPENRESTY_ORBPF_KO_VER)
	tar -czf openresty-orbpf-ko_$(OPENRESTY_ORBPF_KO_VER).orig.tar.gz openresty-orbpf-ko_$(OPENRESTY_ORBPF_KO_VER)

openresty-orbpf-ko-clean:
	-cd openresty-orbpf-ko && debclean
	-find openresty-orbpf-ko -maxdepth 1 ! -name 'debian' ! -name 'openresty-orbpf-ko' -print | xargs rm -rf
	rm -rf openresty-orbpf-ko*.deb
	rm -rf openresty-orbpf-ko_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-orbpf-ko-build
openresty-orbpf-ko-build: openresty-orbpf-ko-clean openresty-orbpf-ko-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-orbpf-ko_$(OPENRESTY_ORBPF_KO_VER).orig.tar.gz --strip-components=1 -C openresty-orbpf-ko
	cd openresty-orbpf-ko \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
