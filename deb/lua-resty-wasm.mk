## Author: spec2deb.pl
### Version: 0.01

LUA_RESTY_WASM_VER := 0.0.1

.PHONY: lua-resty-wasm-download
lua-resty-wasm-download:
	rsync -a -e "ssh -o StrictHostKeyChecking=no -o 'UserKnownHostsFile /dev/null'" nuc:~/work/lua-resty-wasm-$(LUA_RESTY_WASM_VER).tar.gz ./
	rm -rf lua-resty-wasm_$(LUA_RESTY_WASM_VER)
	mkdir -p lua-resty-wasm_$(LUA_RESTY_WASM_VER)
	tar -xf lua-resty-wasm-$(LUA_RESTY_WASM_VER).tar.gz --strip-components=1 -C lua-resty-wasm_$(LUA_RESTY_WASM_VER)
	tar -czf lua-resty-wasm_$(LUA_RESTY_WASM_VER).orig.tar.gz lua-resty-wasm_$(LUA_RESTY_WASM_VER)

lua-resty-wasm-clean:
	-cd lua-resty-wasm && debclean
	-find lua-resty-wasm -maxdepth 1 ! -name 'debian' ! -name 'lua-resty-wasm' -print | xargs rm -rf
	rm -rf lua-resty-wasm*.deb
	rm -rf lua-resty-wasm_*.*

.PHONY: lua-resty-wasm-build
lua-resty-wasm-build: lua-resty-wasm-clean lua-resty-wasm-download
	sudo apt-get -y -q install openresty-elf-loader-dev openresty-elfutils-dev
	sudo apt-get -y -q install --only-upgrade openresty-elf-loader-dev openresty-elfutils-dev
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf lua-resty-wasm_$(LUA_RESTY_WASM_VER).orig.tar.gz --strip-components=1 -C lua-resty-wasm
	cd lua-resty-wasm \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
