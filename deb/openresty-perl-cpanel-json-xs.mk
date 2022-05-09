## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_CPANEL_JSON_XS_VER := 4.28

.PHONY: openresty-perl-cpanel-json-xs-download
openresty-perl-cpanel-json-xs-download:
	LANG=C LC_ALL='C.UTF-8' wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Cpanel-JSON-XS-$(OPENRESTY_PERL_CPANEL_JSON_XS_VER).tar.gz'
	rm -rf openresty-perl-cpanel-json-xs_$(OPENRESTY_PERL_CPANEL_JSON_XS_VER)
	mkdir -p openresty-perl-cpanel-json-xs_$(OPENRESTY_PERL_CPANEL_JSON_XS_VER)
	tar -xf Cpanel-JSON-XS-$(OPENRESTY_PERL_CPANEL_JSON_XS_VER).tar.gz --strip-components=1 -C openresty-perl-cpanel-json-xs_$(OPENRESTY_PERL_CPANEL_JSON_XS_VER)
	tar -czf openresty-perl-cpanel-json-xs_$(OPENRESTY_PERL_CPANEL_JSON_XS_VER).orig.tar.gz openresty-perl-cpanel-json-xs_$(OPENRESTY_PERL_CPANEL_JSON_XS_VER)

openresty-perl-cpanel-json-xs-clean:
	-cd openresty-perl-cpanel-json-xs && debclean
	-find openresty-perl-cpanel-json-xs -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-cpanel-json-xs' -print | xargs rm -rf
	rm -rf openresty-perl-cpanel-json-xs*.deb
	rm -rf openresty-perl-cpanel-json-xs_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.phony: openresty-perl-cpanel-json-xs-build
openresty-perl-cpanel-json-xs-build: openresty-perl-cpanel-json-xs-clean openresty-perl-cpanel-json-xs-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-cpanel-json-xs_$(OPENRESTY_PERL_CPANEL_JSON_XS_VER).orig.tar.gz --strip-components=1 -C openresty-perl-cpanel-json-xs
	cd openresty-perl-cpanel-json-xs \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
