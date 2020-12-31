## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PYTHON3_XRAY_STATS_VER := 0.0.3

.PHONY: openresty-python3-xray-stats-download
openresty-python3-xray-stats-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/python-xray-stats-$(OPENRESTY_PYTHON3_XRAY_STATS_VER).tar.gz ./
	rm -rf openresty-python3-xray-stats_$(OPENRESTY_PYTHON3_XRAY_STATS_VER)
	mkdir -p openresty-python3-xray-stats_$(OPENRESTY_PYTHON3_XRAY_STATS_VER)
	tar -xf python-xray-stats-$(OPENRESTY_PYTHON3_XRAY_STATS_VER).tar.gz --strip-components=1 -C openresty-python3-xray-stats_$(OPENRESTY_PYTHON3_XRAY_STATS_VER)
	tar -czf openresty-python3-xray-stats_$(OPENRESTY_PYTHON3_XRAY_STATS_VER).orig.tar.gz openresty-python3-xray-stats_$(OPENRESTY_PYTHON3_XRAY_STATS_VER)

openresty-python3-xray-stats-clean:
	-cd openresty-python3-xray-stats && debclean
	-find openresty-python3-xray-stats -maxdepth 1 ! -name 'debian' ! -name 'openresty-python3-xray-stats' -print | xargs rm -rf
	rm -rf openresty-python3-xray-stats*.deb
	rm -rf openresty-python3-xray-stats_*.*

.PHONY: openresty-python3-xray-stats-build
openresty-python3-xray-stats-build: openresty-python3-xray-stats-clean openresty-python3-xray-stats-download
	sudo apt-get -y -q install g++ openresty-python3-setuptools
	sudo apt-get -y -q upgrade g++ openresty-python3-setuptools
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-python3-xray-stats_$(OPENRESTY_PYTHON3_XRAY_STATS_VER).orig.tar.gz --strip-components=1 -C openresty-python3-xray-stats
	cd openresty-python3-xray-stats \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
