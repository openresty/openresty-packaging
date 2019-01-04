### Makefile ---

## Author: shell@xps13
## Version: $Id: Makefile,v 0.0 2017/03/22 04:56:03 shell Exp $
## Keywords:
## X-URL:

# you need to install the libtemplate-perl package first to get the tpage utility.
# we use Perl TT2 templates to generate */debian/changelog files.

JOBS=8
ZLIB_VER=1.2.11
PCRE_VER=8.42
SSL_VER=1.1.0h
PLUS_SSL_VER=1.0.2k
OR_VER=1.13.6.1
OR_PLUS_VER=1.13.6.2.48
LEMPLATE_VER=0.15
TEST_NGINX_VER=0.26
ELFUTILS_VER=0.173
STAP_VER=4.0.0.1
HYPERSCAN_VER=5.0.0
OPTS=-sa
DISTRO:=$(shell lsb_release -c|awk '{print $$2}')

.PHONY: build
build: zlib-build pcre-build openssl-build \
	openssl-debug-build openresty-build openresty-debug-build \
	openresty-valgrind-build openresty-plus-build \
	lemplate-build test-nginx-build \
	openresty-plus-debug-build hyperscan-build

.PHONY: clean
clean: zlib-clean pcre-clean openssl-clean openssl-debug-clean \
	openresty-clean openresty-debug-clean openresty-valgrind-clean \
	openresty-plus-clean openresty-plus-debug-clean \
	lemplate-clean test-nginx-clean hyperscan-clean

.PHONY: zlib-download
zlib-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'http://www.zlib.net/fossils/zlib-$(ZLIB_VER).tar.gz'
	cp zlib-$(ZLIB_VER).tar.gz openresty-zlib_$(ZLIB_VER).orig.tar.gz

.PHONY: zlib-build
zlib-build: | zlib-clean zlib-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-zlib_$(ZLIB_VER).orig.tar.gz --strip-components=1 -C openresty-zlib
	cd openresty-zlib \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
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
	wget -nH --cut-dirs=100 --mirror 'https://ftp.pcre.org/pub/pcre/pcre-$(PCRE_VER).tar.bz2'
	cp pcre-$(PCRE_VER).tar.bz2 openresty-pcre_$(PCRE_VER).orig.tar.bz2

.PHONY: pcre-build
pcre-build: | pcre-clean pcre-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-pcre_$(PCRE_VER).orig.tar.bz2 --strip-components=1 -C openresty-pcre
	cd openresty-pcre \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty-pcre*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: pcre-clean
pcre-clean:
	cd openresty-pcre && debclean
	find openresty-pcre -maxdepth 1 ! -name 'debian' ! -name 'openresty-pcre' -print | xargs rm -rf
	rm -f openresty-pcre*.deb
	rm -f openresty-pcre_*.*
	#rm -f pcre-$(PCRE_VER).tar.bz2

.PHONY: plus-openssl-download
plus-openssl-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(PLUS_SSL_VER).tar.gz'
	cp openssl-$(PLUS_SSL_VER).tar.gz openresty-plus-openssl_$(PLUS_SSL_VER).orig.tar.gz

.PHONY: plus-openssl-build
plus-openssl-build: | plus-openssl-clean plus-openssl-download
	sudo apt-get -y -qq install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-openssl_$(PLUS_SSL_VER).orig.tar.gz --strip-components=1 -C openresty-plus-openssl
	cd openresty-plus-openssl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty-openssl*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: plus-openssl-clean
plus-openssl-clean:
	cd openresty-plus-openssl && debclean
	find openresty-plus-openssl -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-openssl' -print | xargs rm -rf
	rm -f openresty-plus-openssl*.deb
	rm -f openresty-plus-openssl_*.*

.PHONY: plus-openssl-debug-download
plus-openssl-debug-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(PLUS_SSL_VER).tar.gz'
	cp openssl-$(PLUS_SSL_VER).tar.gz openresty-plus-openssl-debug_$(PLUS_SSL_VER).orig.tar.gz

.PHONY: plus-openssl-debug-build
plus-openssl-debug-build: | plus-openssl-debug-clean plus-openssl-debug-download
	sudo apt-get -y -qq install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-openssl-debug_$(PLUS_SSL_VER).orig.tar.gz --strip-components=1 -C openresty-plus-openssl-debug
	cd openresty-plus-openssl-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty-openssl*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: plus-openssl-debug-clean
plus-openssl-debug-clean:
	cd openresty-plus-openssl-debug && debclean
	find openresty-plus-openssl-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-openssl-debug' -print | xargs rm -rf
	rm -f openresty-plus-openssl-debug*.deb
	rm -f openresty-plus-openssl-debug_*.*

.PHONY: openssl-download
openssl-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://www.openssl.org/source/openssl-$(SSL_VER).tar.gz'
	cp openssl-$(SSL_VER).tar.gz openresty-openssl_$(SSL_VER).orig.tar.gz

.PHONY: openssl-build
openssl-build: | openssl-clean openssl-download
	sudo apt-get -y -qq install openresty-zlib-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-openssl_$(SSL_VER).orig.tar.gz --strip-components=1 -C openresty-openssl
	cd openresty-openssl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
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
		&& debuild $(OPTS) -j$(JOBS)
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

.PHONY: openresty-download
openresty-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://openresty.org/download/openresty-$(OR_VER).tar.gz'
	cp openresty-$(OR_VER).tar.gz openresty_$(OR_VER).orig.tar.gz

.PHONY: openresty-build
openresty-build: | openresty-clean openresty-download
	sudo apt-get -y -qq install openresty-zlib-dev openresty-pcre-dev openresty-openssl-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty_$(OR_VER).orig.tar.gz --strip-components=1 -C openresty
	cd openresty \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-clean
openresty-clean:
	cd openresty && debclean
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
	sudo apt-get -y -qq install openresty-zlib-dev openresty-pcre-dev openresty-openssl-debug-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-debug_$(OR_VER).orig.tar.gz --strip-components=1 -C openresty-debug
	cd openresty-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty-debug*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-debug-clean
openresty-debug-clean:
	-cd openresty-debug && debclean
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
	sudo apt-get -y -qq install openresty-zlib-dev openresty-pcre-dev openresty-openssl-debug-dev valgrind
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-valgrind_$(OR_VER).orig.tar.gz --strip-components=1 -C openresty-valgrind
	cd openresty-valgrind \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty-valgrind*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-valgrind-clean
openresty-valgrind-clean:
	-cd openresty-valgrind && debclean
	find openresty-valgrind -maxdepth 1 ! -name 'debian' ! -name 'openresty-valgrind' -print | xargs rm -rf
	rm -f openresty-valgrind*.deb
	rm -f openresty-valgrind_*.*

.PHONY: openresty-plus-build
openresty-plus-build: | openresty-plus-clean openresty-plus-download
	sudo apt-get -y -qq install openresty-zlib-dev openresty-pcre-dev openresty-plus-openssl-dev libgd-dev openresty-plus-hyperscan-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus_$(OR_PLUS_VER).orig.tar.gz --strip-components=1 -C openresty-plus
	cd openresty-plus \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload-proprietary ]; then ./upload-proprietary || exit 1; fi

.PHONY: openresty-plus-clean
openresty-plus-clean:
	cd openresty-plus && debclean
	find openresty-plus -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus' -print | xargs rm -rf
	rm -f openresty-plus*.deb
	rm -f openresty-plus_*.*

.PHONY: openresty-plus-download
openresty-plus-download:
	rm -f *.orig.tar.*
	rsync -crlvpP nuc:~/work/openresty-plus-$(OR_PLUS_VER).tar.gz .
	cp openresty-plus-$(OR_PLUS_VER).tar.gz openresty-plus_$(OR_PLUS_VER).orig.tar.gz

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

.PHONY: lemplate-build
lemplate-build: | lemplate-clean lemplate-download
	sudo apt-get -y -qq install libipc-run3-perl libfile-find-rule-perl libtext-glob-perl libnumber-compare-perl
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf liblemplate-perl_$(LEMPLATE_VER).orig.tar.gz --strip-components=1 -C liblemplate-perl
	cd liblemplate-perl \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty-valgrind*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

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
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty-valgrind*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: openresty-plus-debug-build
openresty-plus-debug-build: | openresty-plus-debug-clean openresty-plus-debug-download
	sudo apt-get -y -qq install openresty-zlib-dev openresty-pcre-dev openresty-plus-openssl-debug-dev libgd-dev openresty-plus-hyperscan-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-plus-debug_$(OR_PLUS_VER).orig.tar.gz --strip-components=1 -C openresty-plus-debug
	cd openresty-plus-debug \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in openresty*.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload-proprietary ]; then ./upload-proprietary || exit 1; fi

.PHONY: openresty-plus-debug-clean
openresty-plus-debug-clean:
	cd openresty-plus-debug && debclean
	find openresty-plus-debug -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-debug' -print | xargs rm -rf
	rm -f openresty-plus-debug*.deb
	rm -f openresty-plus-debug_*.*

.PHONY: openresty-plus-debug-download
openresty-plus-debug-download:
	rm -f *.orig.tar.*
	rsync -crlvpP nuc:~/work/openresty-plus-$(OR_PLUS_VER).tar.gz .
	cp openresty-plus-$(OR_PLUS_VER).tar.gz openresty-plus-debug_$(OR_PLUS_VER).orig.tar.gz

.PHONY: stap-download
stap-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://sourceware.org/elfutils/ftp/$(ELFUTILS_VER)/elfutils-$(ELFUTILS_VER).tar.bz2'
	cp elfutils-$(ELFUTILS_VER).tar.bz2 openresty-stap-elfutils_$(ELFUTILS_VER).orig.tar.bz2
	rsync -crlvpP nuc:~/work/systemtap-plus-$(STAP_VER).tar.gz .
	cp systemtap-plus-$(STAP_VER).tar.gz openresty-stap-$(STAP_VER).orig.tar.gz

.PHONY: stap-build
stap-build: | stap-clean stap-download
	sudo apt-get -y -qq install libnss3-dev libnspr4-dev libnss3-tools libavahi-client-dev m4
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	mkdir openresty-stap-elfutils
	tar xf openresty-stap-elfutils_$(ELFUTILS_VER).orig.tar.bz2 --strip-components=1 -C openresty-stap-elfutils
	tar xf openresty-stap-$(STAP_VER).orig.tar.gz --strip-components=1 -C openresty-stap
	cd openresty-stap \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in *.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: stap-clean
stap-clean:
	cd openresty-stap && debclean
	find openresty-stap -maxdepth 1 ! -name 'debian' ! -name 'openresty-stap' -print | xargs rm -rf
	rm -f openresty-stap*.deb
	rm -f openresty-stap_*.*
	rm -rf openresty-stap-elfutils

.PHONY: hyperscan-download
hyperscan-download:
	rm -f *.orig.tar.*
	wget -nH --cut-dirs=100 --mirror 'https://github.com/intel/hyperscan/archive/v$(HYPERSCAN_VER).tar.gz'
	cp v$(HYPERSCAN_VER).tar.gz openresty-plus-hyperscan_$(HYPERSCAN_VER).orig.tar.gz

.PHONY: hyperscan-build
hyperscan-build: | hyperscan-clean hyperscan-download
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	sudo apt-get -y -qq install cmake ragel libboost-dev python libsqlite3-dev
	tar xf openresty-plus-hyperscan_$(HYPERSCAN_VER).orig.tar.gz --strip-components=1 -C openresty-plus-hyperscan
	cd openresty-plus-hyperscan \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#for f in *.deb; do debsigs --sign=origin -K D5EDEB74 $$f || exit 1; done
	if [ -f ./upload ]; then ./upload || exit 1; fi

.PHONY: hyperscan-clean
hyperscan-clean:
	cd openresty-plus-hyperscan && debclean
	find openresty-plus-hyperscan -maxdepth 1 ! -name 'debian' ! -name 'openresty-plus-hyperscan' -print | xargs rm -rf
	rm -f openresty-plus-hyperscan*.deb
	rm -f openresty-plus-hyperscan_*.*

### Makefile ends here
