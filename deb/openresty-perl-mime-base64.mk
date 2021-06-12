## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_PERL_MIME_BASE64_VER := 3.16

.PHONY: openresty-perl-mime-base64-download
openresty-perl-mime-base64-download:
	wget -nH --cut-dirs=100 --mirror 'https://cpan.metacpan.org/authors/id/C/CA/CAPOEIRAB/MIME-Base64-$(OPENRESTY_PERL_MIME_BASE64_VER).tar.gz'
	rm -rf openresty-perl-mime-base64_$(OPENRESTY_PERL_MIME_BASE64_VER)
	mkdir -p openresty-perl-mime-base64_$(OPENRESTY_PERL_MIME_BASE64_VER)
	tar -xf MIME-Base64-$(OPENRESTY_PERL_MIME_BASE64_VER).tar.gz --strip-components=1 -C openresty-perl-mime-base64_$(OPENRESTY_PERL_MIME_BASE64_VER)
	tar -czf openresty-perl-mime-base64_$(OPENRESTY_PERL_MIME_BASE64_VER).orig.tar.gz openresty-perl-mime-base64_$(OPENRESTY_PERL_MIME_BASE64_VER)

openresty-perl-mime-base64-clean:
	-cd openresty-perl-mime-base64 && debclean
	-find openresty-perl-mime-base64 -maxdepth 1 ! -name 'debian' ! -name 'openresty-perl-mime-base64' -print | xargs rm -rf
	rm -rf openresty-perl-mime-base64*.deb
	rm -rf openresty-perl-mime-base64_*.*

.PHONY: openresty-perl-mime-base64-build
openresty-perl-mime-base64-build: openresty-perl-mime-base64-clean openresty-perl-mime-base64-download
	sudo apt-get -y -q install openresty-perl openresty-perl-dev
	sudo apt-get -y -q install --only-upgrade openresty-perl openresty-perl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-perl-mime-base64_$(OPENRESTY_PERL_MIME_BASE64_VER).orig.tar.gz --strip-components=1 -C openresty-perl-mime-base64
	cd openresty-perl-mime-base64 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
