## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_LLVM_VER := 14.0.0.1

.PHONY: openresty-llvm-download
openresty-llvm-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/llvm-plus-$(OPENRESTY_LLVM_VER).tar.gz ./
	rm -rf openresty-llvm_$(OPENRESTY_LLVM_VER)
	mkdir -p openresty-llvm_$(OPENRESTY_LLVM_VER)
	tar -xf llvm-plus-$(OPENRESTY_LLVM_VER).tar.gz --strip-components=1 -C openresty-llvm_$(OPENRESTY_LLVM_VER)
	tar -czf openresty-llvm_$(OPENRESTY_LLVM_VER).orig.tar.gz openresty-llvm_$(OPENRESTY_LLVM_VER)

openresty-llvm-clean:
	-cd openresty-llvm && debclean
	-find openresty-llvm -maxdepth 1 ! -name 'debian' ! -name 'openresty-llvm' -print | xargs rm -rf
	rm -rf openresty-llvm*.deb
	rm -rf openresty-llvm_*.*

#sudo apt-get -y -q install libtemplate-perl debhelper devscripts dh-systemd
#sudo apt-get -y -q install --only-upgrade libtemplate-perl debhelper devscripts dh-systemd
.PHONY: openresty-llvm-build
openresty-llvm-build: openresty-llvm-clean openresty-llvm-download
	sudo apt-get -y -q install gcc g++ clang ccache cmake zlib1g-dev libffi-dev libncurses-dev binutils-dev
	sudo apt-get -y -q install --only-upgrade gcc g++ clang ccache cmake zlib1g-dev libffi-dev libncurses-dev binutils-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-llvm_$(OPENRESTY_LLVM_VER).orig.tar.gz --strip-components=1 -C openresty-llvm
	cd openresty-llvm \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
