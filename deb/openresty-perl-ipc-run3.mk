## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_IPC_RUN3_VER := 0.049

.PHONY: openresty-perl-ipc-run3-download
openresty-perl-ipc-run3-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/R/RJ/RJBS/IPC-Run3-$(OPENRESTY_PERL_IPC_RUN3_VER).tar.gz'
	rm -rf openresty-perl-ipc-run3_$(OPENRESTY_PERL_IPC_RUN3_VER)
	mkdir -p openresty-perl-ipc-run3_$(OPENRESTY_PERL_IPC_RUN3_VER)
	tar -xf IPC-Run3-$(OPENRESTY_PERL_IPC_RUN3_VER).tar.gz --strip-components=1 -C openresty-perl-ipc-run3_$(OPENRESTY_PERL_IPC_RUN3_VER)
	tar -czf openresty-perl-ipc-run3_$(OPENRESTY_PERL_IPC_RUN3_VER).orig.tar.gz openresty-perl-ipc-run3_$(OPENRESTY_PERL_IPC_RUN3_VER)

openresty-perl-ipc-run3-clean:
	-cd openresty-perl-ipc-run3 && debclean
	-find openresty-perl-ipc-run3 -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-ipc-run3' -print | xargs rm -rf
	rm -rf openresty-perl-ipc-run3*.deb
	rm -rf openresty-perl-ipc-run3_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-perl-ipc-run3-build
openresty-perl-ipc-run3-build: openresty-perl-ipc-run3-clean openresty-perl-ipc-run3-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-ipc-run3_$(OPENRESTY_PERL_IPC_RUN3_VER).orig.tar.gz --strip-components=1 -C openresty-perl-ipc-run3
	cd openresty-perl-ipc-run3 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
