## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_IPC_RUN_VER := 20200505.0

.PHONY: openresty-perl-ipc-run-download
openresty-perl-ipc-run-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/T/TO/TODDR/IPC-Run-$(OPENRESTY_PERL_IPC_RUN_VER).tar.gz'
	rm -rf openresty-perl-ipc-run_$(OPENRESTY_PERL_IPC_RUN_VER)
	mkdir -p openresty-perl-ipc-run_$(OPENRESTY_PERL_IPC_RUN_VER)
	tar -xf IPC-Run-$(OPENRESTY_PERL_IPC_RUN_VER).tar.gz --strip-components=1 -C openresty-perl-ipc-run_$(OPENRESTY_PERL_IPC_RUN_VER)
	tar -czf openresty-perl-ipc-run_$(OPENRESTY_PERL_IPC_RUN_VER).orig.tar.gz openresty-perl-ipc-run_$(OPENRESTY_PERL_IPC_RUN_VER)

openresty-perl-ipc-run-clean:
	-cd openresty-perl-ipc-run && debclean
	-find openresty-perl-ipc-run -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-ipc-run' -print | xargs rm -rf
	rm -rf openresty-perl-ipc-run*.deb
	rm -rf openresty-perl-ipc-run_*.*

.PHONY: openresty-perl-ipc-run-build
openresty-perl-ipc-run-build: openresty-perl-ipc-run-clean openresty-perl-ipc-run-download
	sudo apt-get -y -q install openresty-perl openresty-perl-readonly
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-readonly
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-ipc-run_$(OPENRESTY_PERL_IPC_RUN_VER).orig.tar.gz --strip-components=1 -C openresty-perl-ipc-run
	cd openresty-perl-ipc-run \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
