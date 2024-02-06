## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_RADARE2_R2DEC_VER := 0.0.1

.PHONY: openresty-radare2-r2dec-download
openresty-radare2-r2dec-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/r2dec-js-plus-$(OPENRESTY_RADARE2_R2DEC_VER).tar.gz ./
	rm -rf openresty-radare2-r2dec_$(OPENRESTY_RADARE2_R2DEC_VER)
	mkdir -p openresty-radare2-r2dec_$(OPENRESTY_RADARE2_R2DEC_VER)
	tar -xf r2dec-js-plus-$(OPENRESTY_RADARE2_R2DEC_VER).tar.gz --strip-components=1 -C openresty-radare2-r2dec_$(OPENRESTY_RADARE2_R2DEC_VER)
	tar -czf openresty-radare2-r2dec_$(OPENRESTY_RADARE2_R2DEC_VER).orig.tar.gz openresty-radare2-r2dec_$(OPENRESTY_RADARE2_R2DEC_VER)

openresty-radare2-r2dec-clean:
	-cd openresty-radare2-r2dec && debclean
	-find openresty-radare2-r2dec -maxdepth 1 ! -name 'debian' ! -name 'openresty-radare2-r2dec' -print | xargs rm -rf
	rm -rf openresty-radare2-r2dec*.deb
	rm -rf openresty-radare2-r2dec_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-radare2-r2dec-build
openresty-radare2-r2dec-build: openresty-radare2-r2dec-clean openresty-radare2-r2dec-download
	sudo apt-get -y -q install wget openresty-python3 openresty-radare2-dev
	sudo apt-get -y -q install --only-upgrade wget openresty-python3 openresty-radare2-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-radare2-r2dec_$(OPENRESTY_RADARE2_R2DEC_VER).orig.tar.gz --strip-components=1 -C openresty-radare2-r2dec
	cd openresty-radare2-r2dec \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
