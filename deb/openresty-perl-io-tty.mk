## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_IO_TTY_VER := 1.16

.PHONY: openresty-perl-io-tty-download
openresty-perl-io-tty-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/T/TO/TODDR/IO-Tty-$(OPENRESTY_PERL_IO_TTY_VER).tar.gz'
	rm -rf openresty-perl-io-tty_$(OPENRESTY_PERL_IO_TTY_VER)
	mkdir -p openresty-perl-io-tty_$(OPENRESTY_PERL_IO_TTY_VER)
	tar -xf IO-Tty-$(OPENRESTY_PERL_IO_TTY_VER).tar.gz --strip-components=1 -C openresty-perl-io-tty_$(OPENRESTY_PERL_IO_TTY_VER)
	tar -czf openresty-perl-io-tty_$(OPENRESTY_PERL_IO_TTY_VER).orig.tar.gz openresty-perl-io-tty_$(OPENRESTY_PERL_IO_TTY_VER)

openresty-perl-io-tty-clean:
	-cd openresty-perl-io-tty && debclean
	-find openresty-perl-io-tty -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-io-tty' -print | xargs rm -rf
	rm -rf openresty-perl-io-tty*.deb
	rm -rf openresty-perl-io-tty_*.*

.PHONY: openresty-perl-io-tty-build
openresty-perl-io-tty-build: openresty-perl-io-tty-clean openresty-perl-io-tty-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-io-tty_$(OPENRESTY_PERL_IO_TTY_VER).orig.tar.gz --strip-components=1 -C openresty-perl-io-tty
	cd openresty-perl-io-tty \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
