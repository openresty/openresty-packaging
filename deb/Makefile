### Makefile ---

## Author: shell@xps13
## Version: $Id: Makefile,v 0.0 2017/03/22 04:56:03 shell Exp $
## Keywords:
## X-URL:

# you need to install the libtemplate-perl package first to get the tpage utility.
# we use Perl TT2 templates to generate */debian/changelog files.

JOBS=$(shell nproc)
ZLIB_VER=1.3.1
PCRE_VER=8.45
SSL_VER=1.1.0l
SSL111_VER=1.1.1w
SSL3_VER=3.5.1
OR_VER=1.27.1.2
LEMPLATE_VER=0.15
TEST_NGINX_VER=0.29
OPTS=
DISTRO:=$(shell lsb_release -c|awk '{print $$2}')
deb_toolchain_pkgs = debhelper devscripts

.PHONY: build
build: zlib-build pcre-build openssl-build \
	openssl-debug-build openresty-build openresty-debug-build \
	openresty-valgrind-build \
	lemplate-build test-nginx-build openresty-pcre2-build

.PHONY: clean
clean: zlib-clean pcre-clean openssl-clean openssl-debug-clean \
		openresty-clean openresty-debug-clean openresty-valgrind-clean \
		lemplate-clean test-nginx-clean \
		openssl111-clean openssl111-debug-clean  \
		openresty-zlib-asan-clean openresty-pcre-asan-clean \
		openresty-openssl111-asan-clean openresty-asan-clean \
		openresty-pcre2-asan-clean \
		openresty-pcre2-clean openresty-openssl3-clean \
		openresty-openssl3-asan-clean openresty-openssl3-debug-clean
	-rm -f *.gz *.bz2 *.xz *.zip

.PHONY: zlib-download
zlib-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.zlib.net/fossils/zlib-$(ZLIB_VER).tar.gz'
	cp zlib-$(ZLIB_VER).tar.gz openresty-zlib_$(ZLIB_VER).orig.tar.gz

.PHONY: openresty-zlib-build
openresty-zlib-build: zlib-build

.PHONY: zlib-build
zlib-build: | zlib-clean zlib-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	sudo apt-get -qq -y install autotools-dev
	tar xf openresty-zlib_$(ZLIB_VER).orig.tar.gz --strip-components=1 -C openresty-zlib
	cd openresty-zlib \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#for f in *.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: zlib-clean
zlib-clean:
	cd openresty-zlib && debclean
	find openresty-zlib -maxdepth 1 ! -name 'debian' ! -name 'openresty-zlib' -print | xargs rm -rf
	rm -f openresty-zlib*.deb
	rm -f openresty-zlib_*.*
	#rm -f zlib-$(ZLIB_VER).tar.gz

.PHONY: pcre-download
pcre-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://sourceforge.net/projects/pcre/files/pcre/$(PCRE_VER)/pcre-$(PCRE_VER).tar.bz2'
	cp pcre-$(PCRE_VER).tar.bz2 openresty-pcre_$(PCRE_VER).orig.tar.bz2

.PHONY: openresty-pcre-build
openresty-pcre-build: pcre-build

.PHONY: pcre-build
pcre-build: | pcre-clean pcre-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-pcre_$(PCRE_VER).orig.tar.bz2 --strip-components=1 -C openresty-pcre
	cd openresty-pcre \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#for f in openresty-pcre*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: pcre-clean
pcre-clean:
	cd openresty-pcre && debclean
	find openresty-pcre -maxdepth 1 ! -name 'debian' ! -name 'openresty-pcre' -print | xargs rm -rf
	rm -f openresty-pcre*.deb
	rm -f openresty-pcre_*.*
	#rm -f pcre-$(PCRE_VER).tar.bz2

.PHONY: openssl-download
openssl-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(SSL_VER).tar.gz'
	cp openssl-$(SSL_VER).tar.gz openresty-openssl_$(SSL_VER).orig.tar.gz

.PHONY: openresty-openssl-build
openresty-openssl-build: openssl-build

.PHONY: openssl-build
openssl-build: | openssl-clean openssl-download
	sudo apt-get -y -qq install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl_$(SSL_VER).orig.tar.gz --strip-components=1 -C openresty-openssl
	cd openresty-openssl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#for f in openresty-openssl*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openssl-debug-download
openssl-debug-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(SSL_VER).tar.gz'
	cp openssl-$(SSL_VER).tar.gz openresty-openssl-debug_$(SSL_VER).orig.tar.gz

.PHONY: openssl-debug-build
openssl-debug-build: | openssl-debug-clean openssl-debug-download
	sudo apt-get -y -qq install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl-debug_$(SSL_VER).orig.tar.gz --strip-components=1 -C openresty-openssl-debug
	cd openresty-openssl-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian -sa $(OPTS) -j$(JOBS)
	#for f in openresty-openssl-debug*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openssl-clean
openssl-clean:
	cd openresty-openssl && debclean
	find openresty-openssl -maxdepth 1 ! -name 'debian' ! -name 'openresty-openssl' -print | xargs rm -rf
	rm -f openresty-openssl*.deb
	rm -f openresty-openssl_*.*

.PHONY: openssl-debug-clean
openssl-debug-clean:
	-cd openresty-openssl-debug && debclean
	find openresty-openssl-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-openssl-debug' -print | xargs rm -rf
	rm -f openresty-openssl*.deb
	rm -f openresty-openssl-debug_*.*

.PHONY: openssl111-download
openssl111-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(SSL111_VER).tar.gz'
	cp openssl-$(SSL111_VER).tar.gz openresty-openssl111_$(SSL111_VER).orig.tar.gz

.PHONY: openresty-openssl111-build
openresty-openssl111-build: openssl111-build

.PHONY: openssl111-build
openssl111-build: | openssl111-clean openssl111-download
	sudo apt-get -y -qq install openresty-zlib-dev
	sudo apt-get --only-upgrade -y -qq install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl111_$(SSL111_VER).orig.tar.gz --strip-components=1 -C openresty-openssl111
	cd openresty-openssl111 \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#for f in openresty-openssl111*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openssl111-debug-download
openssl111-debug-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(SSL111_VER).tar.gz'
	cp openssl-$(SSL111_VER).tar.gz openresty-openssl111-debug_$(SSL111_VER).orig.tar.gz

.PHONY: openresty-openssl111-debug-build
openresty-openssl111-debug-build: openssl111-debug-build

.PHONY: openssl111-debug-build
openssl111-debug-build: | openssl111-debug-clean openssl111-debug-download
	sudo apt-get -y -qq install openresty-zlib-dev
	sudo apt-get -y -qq --only-upgrade install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl111-debug_$(SSL111_VER).orig.tar.gz --strip-components=1 -C openresty-openssl111-debug
	cd openresty-openssl111-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian -sa $(OPTS) -j$(JOBS)
	#for f in openresty-openssl111-debug*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openssl111-clean
openssl111-clean:
	-cd openresty-openssl111 && debclean
	rm -rf openresty-openssl111/debian/tmp openresty-openssl111/test openresty-openssl111/*.a
	find openresty-openssl111 -maxdepth 1 ! -name 'debian' ! -name 'openresty-openssl111' -print | xargs rm -rf
	rm -f openresty-openssl111*.deb
	rm -f openresty-openssl111_*.*

.PHONY: openssl111-debug-clean
openssl111-debug-clean:
	-cd openresty-openssl111-debug && debclean
	rm -rf openresty-openssl111-debug/debian/tmp openresty-openssl111-debug/test openresty-openssl111-debug/*.a
	find openresty-openssl111-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-openssl111-debug' -print | xargs rm -rf
	rm -f openresty-openssl111*.deb
	rm -f openresty-openssl111-debug_*.*

.PHONY: openresty-download
openresty-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-$(OR_VER).tar.gz'
	cp openresty-$(OR_VER).tar.gz openresty_$(OR_VER).orig.tar.gz

.PHONY: openresty-build
openresty-build: | openresty-clean openresty-download
	sudo apt-get -y -qq install openresty-zlib-dev openresty-pcre2-dev openresty-openssl3-dev systemtap-sdt-dev $(deb_toolchain_pkgs)
	sudo apt-get -y -qq --only-upgrade install openresty-zlib-dev openresty-pcre2-dev openresty-openssl3-dev systemtap-sdt-dev $(deb_toolchain_pkgs)
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty_$(OR_VER).orig.tar.gz --strip-components=1 -C openresty
	cd openresty \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian $(OPTS) -j$(JOBS)
	#for f in openresty*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-clean
openresty-clean:
	cd openresty && debclean || true
	find openresty -maxdepth 1 ! -name 'debian' ! -name 'openresty' -print | xargs rm -rf
	rm -f openresty*.deb
	rm -f openresty_*.*

.PHONY: openresty-debug-download
openresty-debug-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-$(OR_VER).tar.gz'
	cp openresty-$(OR_VER).tar.gz openresty-debug_$(OR_VER).orig.tar.gz

.PHONY: openresty-debug-build
openresty-debug-build: | openresty-debug-clean openresty-debug-download
	sudo apt-get -y -qq install openresty-zlib-dev openresty-pcre2-dev openresty-openssl3-debug-dev
	sudo apt-get -y -qq --only-upgrade install openresty-zlib-dev openresty-pcre2-dev openresty-openssl3-debug-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-debug_$(OR_VER).orig.tar.gz --strip-components=1 -C openresty-debug
	cd openresty-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian -sa $(OPTS) -j$(JOBS)
	#for f in openresty-debug*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-debug-clean
openresty-debug-clean:
	-cd openresty-debug && debclean || true
	find openresty-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-debug' -print | xargs rm -rf
	rm -f openresty-debug*.deb
	rm -f openresty-debug_*.*

.PHONY: openresty-valgrind-download
openresty-valgrind-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-$(OR_VER).tar.gz'
	cp openresty-$(OR_VER).tar.gz openresty-valgrind_$(OR_VER).orig.tar.gz

.PHONY: openresty-valgrind-build
openresty-valgrind-build: | openresty-valgrind-clean openresty-valgrind-download
	sudo apt-get -y -qq install openresty-zlib-dev openresty-pcre2-dev openresty-openssl3-debug-dev valgrind
	sudo apt-get -y -qq --only-upgrade install openresty-zlib-dev openresty-pcre2-dev openresty-openssl3-debug-dev valgrind
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-valgrind_$(OR_VER).orig.tar.gz --strip-components=1 -C openresty-valgrind
	cd openresty-valgrind \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian -sa $(OPTS) -j$(JOBS)
	#for f in openresty-valgrind*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-valgrind-clean
openresty-valgrind-clean:
	-cd openresty-valgrind && debclean || true
	find openresty-valgrind -maxdepth 1 ! -name 'debian' ! -name 'openresty-valgrind' -print | xargs rm -rf
	rm -f openresty-valgrind*.deb
	rm -f openresty-valgrind_*.*

.PHONY: lemplate-download
lemplate-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'http://search.cpan.org/CPAN/authors/id/A/AG/AGENT/Lemplate-$(LEMPLATE_VER).tar.gz'
	cp Lemplate-$(LEMPLATE_VER).tar.gz liblemplate-perl_$(LEMPLATE_VER).orig.tar.gz

.PHONY: lemplate-clean
lemplate-clean:
	-cd liblemplate-perl/ && debclean
	find liblemplate-perl -maxdepth 1 ! -name 'debian' ! -name 'liblemplate-perl' -print | xargs rm -rf
	rm -f liblemplate-perl*.deb
	rm -f liblemplate-perl_*.*

.PHONY: liblemplate-perl-build
liblemplate-perl-build: lemplate-build

.PHONY: lemplate-build
lemplate-build: | lemplate-clean lemplate-download
	sudo apt-get -y -qq install libipc-run3-perl libfile-find-rule-perl libtext-glob-perl libnumber-compare-perl
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf liblemplate-perl_$(LEMPLATE_VER).orig.tar.gz --strip-components=1 -C liblemplate-perl
	cd liblemplate-perl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian -sa $(OPTS) -j$(JOBS)
	#for f in openresty-valgrind*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: libtest-nginx-perl-build
libtest-nginx-perl-build: test-nginx-build

.PHONY: test-nginx-download
test-nginx-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'http://search.cpan.org/CPAN/authors/id/A/AG/AGENT/Test-Nginx-$(TEST_NGINX_VER).tar.gz'
	cp Test-Nginx-$(TEST_NGINX_VER).tar.gz libtest-nginx-perl_$(TEST_NGINX_VER).orig.tar.gz

.PHONY: test-nginx-clean
test-nginx-clean:
	-cd libtest-nginx-perl/ && debclean
	find libtest-nginx-perl -maxdepth 1 ! -name 'debian' ! -name 'libtest-nginx-perl' -print | xargs rm -rf
	rm -f libtest-nginx-perl*.deb
	rm -f libtest-nginx-perl_*.*

.PHONY: test-nginx-build
test-nginx-build: | test-nginx-clean test-nginx-download
	sudo apt-get -y -qq install libtest-base-perl libtest-longstring-perl libtext-diff-perl liblist-moreutils-perl
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf libtest-nginx-perl_$(TEST_NGINX_VER).orig.tar.gz --strip-components=1 -C libtest-nginx-perl
	cd libtest-nginx-perl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild --no-lintian -sa $(OPTS) -j$(JOBS)
	#for f in openresty-valgrind*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

include *.mk
### Makefile ends here
