## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PYTHON3_GOTO_VER := 1.2.1

.PHONY: openresty-python3-goto-download
openresty-python3-goto-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/python-goto-plus-$(OPENRESTY_PYTHON3_GOTO_VER).tar.gz ./
	rm -rf openresty-python3-goto_$(OPENRESTY_PYTHON3_GOTO_VER)
	mkdir -p openresty-python3-goto_$(OPENRESTY_PYTHON3_GOTO_VER)
	tar -xf python-goto-plus-$(OPENRESTY_PYTHON3_GOTO_VER).tar.gz --strip-components=1 -C openresty-python3-goto_$(OPENRESTY_PYTHON3_GOTO_VER)
	tar -czf openresty-python3-goto_$(OPENRESTY_PYTHON3_GOTO_VER).orig.tar.gz openresty-python3-goto_$(OPENRESTY_PYTHON3_GOTO_VER)

openresty-python3-goto-clean:
	cd openresty-python3-goto && debclean
	-find openresty-python3-goto -maxdepth 1 ! -name 'debian' ! -name 'openresty-python3-goto' -print | xargs rm -rf
	rm -rf openresty-python3-goto*.deb
	rm -rf openresty-python3-goto_*.*

.PHONY: openresty-python3-goto-build
openresty-python3-goto-build: openresty-python3-goto-clean openresty-python3-goto-download
	sudo apt-get -y -qq install openresty-python3-dev openresty-python3-setuptools
	sudo apt-get -y -qq --only-upgrade install openresty-python3-dev openresty-python3-setuptools
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-python3-goto_$(OPENRESTY_PYTHON3_GOTO_VER).orig.tar.gz --strip-components=1 -C openresty-python3-goto
	cd openresty-python3-goto \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
