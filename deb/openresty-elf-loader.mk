## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_ELF_LOADER_VER := 0.0.2

.PHONY: openresty-elf-loader-download
openresty-elf-loader-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/elf-loader-$(OPENRESTY_ELF_LOADER_VER).tar.gz ./
	rm -rf openresty-elf-loader_$(OPENRESTY_ELF_LOADER_VER)
	mkdir -p openresty-elf-loader_$(OPENRESTY_ELF_LOADER_VER)
	tar -xf elf-loader-$(OPENRESTY_ELF_LOADER_VER).tar.gz --strip-components=1 -C openresty-elf-loader_$(OPENRESTY_ELF_LOADER_VER)
	tar -czf openresty-elf-loader_$(OPENRESTY_ELF_LOADER_VER).orig.tar.gz openresty-elf-loader_$(OPENRESTY_ELF_LOADER_VER)

openresty-elf-loader-clean:
	-cd openresty-elf-loader && debclean
	-find openresty-elf-loader -maxdepth 1 ! -name 'debian' ! -name 'openresty-elf-loader' -print | xargs rm -rf
	rm -rf openresty-elf-loader*.deb
	rm -rf openresty-elf-loader_*.*

.PHONY: openresty-elf-loader-build
openresty-elf-loader-build: openresty-elf-loader-clean openresty-elf-loader-download
	sudo apt-get -y -q install openresty-elfutils-dev
	sudo apt-get -y -q install --only-upgrade openresty-elfutils-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-elf-loader_$(OPENRESTY_ELF_LOADER_VER).orig.tar.gz --strip-components=1 -C openresty-elf-loader
	cd openresty-elf-loader \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
