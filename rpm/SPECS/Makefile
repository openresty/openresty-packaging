rpmbuild_dir := $(shell rpmbuild -E "%{_topdir}")

targets = openresty \
	  openresty-debug \
	  openresty-valgrind \
	  openresty-asan \
	  openresty-openssl \
	  openresty-openssl111 \
	  openresty-openssl-debug \
	  openresty-openssl111-debug \
	  openresty-openssl-asan \
	  openresty-openssl111-asan \
	  openresty-pcre \
	  openresty-pcre2 \
	  openresty-pcre-asan \
	  openresty-zlib \
	  openresty-zlib-asan \
	  perl-Test-Nginx \
	  perl-Lemplate \
	  perl-Test-LongString \
	  perl-Test-Base \
	  perl-Spiffy \
	  perl-Test-Deep \
	  perl-IPC-Run \
	  perl-IO-Tty \
	  perl-Readonly \
	  perl-Test-Simple

priv_targets = \
		openresty-opencc \
		openresty-plzip \
		openresty-yajl \
		openresty-tar \
		openresty-binutils \
		openresty-libdemangle \
		openresty-elfutils \
		openresty-saas-zlib \
		openresty-saas-pcre \
		openresty-saas-pcre2 \
		openresty-plus-openssl \
		openresty-plus-openssl-debug \
		openresty-plus-openssl-asan \
		openresty-plus-openssl111 \
		openresty-plus-openssl111-debug \
		openresty-plus-openssl111-asan \
		openresty-util-linux \
		openresty-utils \
		openresty-python3 \
		openresty-python3-setuptools \
		openresty-python3-cython \
		openresty-python3-goto \
		openresty-python3-numpy \
		openresty-python3-xray-stats \
		openresty-perl \
		openresty-perl-Cpanel-JSON-XS \
		openresty-stap2 \
		openresty-stap \
		openresty-gdb \
		openresty-saas \
		openresty-saas-asan \
		openresty-cyrus-sasl \
		openresty-plus-hyperscan \
		openresty-elf-loader \
		openresty-plus-core \
		openresty-plus-core-h3 \
		openresty-plus-core-test \
		openresty-plus-core-asan \
		openresty-postgresql \
		openresty-postgresql12 \
		openresty-postgresql15 \
		openresty-postgresql16 \
		openresty-postgresql-ip4r \
		openresty-postgresql12-ip4r \
		openresty-postgresql-orsl \
		openresty-postgresql12-orsl \
		openresty-postgresql12-timescaledb \
		openresty-postgresql-timescaledb \
		openresty-postgresql15-ip4r \
		openresty-postgresql15-orsl \
		openresty-postgresql15-timescaledb \
		openresty-postgresql15-auto-failover \
		openresty-postgresql16-ip4r \
		openresty-postgresql16-orsl \
		openresty-postgresql16-timescaledb \
		openresty-postgresql16-auto-failover \
		openresty-odb \
		openresty-odb-debug \
		openresty-libcurl   \
		openresty-firejail \
		openresty-libcco \
		openresty-boringssl \
		openresty-hiredis \
		coro-nginx-module-1.21.4 \
		coro-nginx-module-1.25.3 \
		coro-nginx-module-1.27.1 \
		coro-hiredis-nginx-module-1.21.4 \
		coro-hiredis-nginx-module-1.25.3 \
		coro-hiredis-nginx-module-1.27.1 \
		coro-libcurl-nginx-module-1.21.4 \
		coro-libcurl-nginx-module-1.25.3 \
		coro-libcurl-nginx-module-1.27.1 \
		lua-resty-redis-cluster-fast-1.21.4 \
		lua-resty-redis-cluster-fast-1.25.3 \
		lua-resty-redis-cluster-fast-1.27.1 \
		lua-resty-http-fast-1.21.4 \
		lua-resty-http-fast-1.25.3 \
		lua-resty-http-fast-1.27.1 \
		openresty-libinjection \
		openresty-libinjection-asan \
		openresty-luajit-plus \
		openresty-maxminddb \
		openresty-maxminddb-debug \
		openresty-maxminddb-asan \
		openresty-coreutils \
		openresty-maxminddb-utils \
		openresty-edge-pki \
		openresty-edge-pki-asan \
		openresty-perl-B-Flags \
		openresty-perl-Opcodes \
		openresty-perl-ExtUtils-Config \
		openresty-perl-ExtUtils-Helpers \
		openresty-perl-ExtUtils-InstallPaths \
		openresty-perl-Module-Build-Tiny \
		openresty-perl-Readonly \
		openresty-perl-IO-Tty \
		openresty-perl-IPC-Run \
		openresty-perl-IPC-Run3 \
		openresty-perl-B-C \
		openresty-perl-App-cpanminus \
		openresty-perl-common-sense \
		openresty-perl-Net-SSLeay \
		openresty-perl-IO-Socket-SSL \
		openresty-perl-Types-Serialiser \
		openresty-perl-Canary-Stability \
        openresty-perl-JSON-XS \
		openresty-perl-Mozilla-CA \
		openresty-perl-Protocol-WebSocket \
		openresty-pcap \
		openresty-tcpdump \
		openresty-wrk \
		openresty-tcmalloc \
		openresty-dw2c \
		openresty-libbpf \
		openresty-lua-cjson \
		openresty-keepalived \
		openresty-bpftool \
		openresty-ebpf-plus \
		dymetrics-nginx-module-1.19.9 \
		dymetrics-nginx-module-1.21.4 \
		dymetrics-nginx-module-1.25.3 \
		dymetrics-nginx-module-1.27.1 \
		lua-resty-dymetrics-bilibili \
		openresty-llvm \
		openresty-libbpf-net \
		openresty-bpftool-net \
		openresty-xdp-tools \
		openresty-iproute2 \
		openresty-radare2 \
		openresty-absl \
		openresty-symgen \
		openresty-nodejs \
		openresty-edgcpfe \
		openresty-radare2-r2dec \
		openresty-gdb-runtime \
		openresty-zstd \
		openresty-procsnap \
		openresty-ljsb \
		openresty-librdkafka \
		openresty-otel-nginx-module-1.19.9 \
		openresty-otel-nginx-module-1.27.1 \
		lua-resty-limit-traffic-dynamic \
		openresty-postgresql12-auto-failover \
		lua-kafka-nginx-module-1.21.4 \
		lua-kafka-nginx-module-1.25.3 \
		lua-kafka-nginx-module-1.27.1 \
		replace-filter-plus-nginx-module-1.21.4 \
		replace-filter-plus-nginx-module-1.27.1 \
		openresty-minifiers \
		dubbo-nginx-module-plus-1.25.3 \
		\
		lua-resty-jsonb \
		openresty-perl-MIME-Base64 \
		openresty-plus \
		openresty-plus-debug \
		openresty-plus-test \
		openresty-plus-valgrind \
		openresty-plus-asan \
		openresty-libmemcached \
		lua-resty-wasm \
		openresty-docker \
		openresty-libmariadb \
		openresty-orbpf-ko

.PHONY: all
all: openresty

.PHONY: $(targets)
$(targets):
	#echo $(rpmbuild_dir)
	rm -f ~/rpmbuild/SRPMS/$@-[0-9]*.rpm ~/rpmbuild/RPMS/*/$@*-[0-9].rpm
	spectool -g -R $@.spec
	sudo dnf builddep -y $@.spec
	PATH=/usr/bin:$$PATH time rpmbuild -v -ba $@.spec
	#time rpmbuild -bi --short-circuit $@.spec
	#-cp -v ~/rpmbuild/SRPMS/$@*.src.rpm ~/rpmbuild/RPMS/*/$@*.rpm /tmp/
	ls -lh $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm
	ls -lh $(rpmbuild_dir)/RPMS/*/$@-[0-9]*.rpm
	for f in $(rpmbuild_dir)/RPMS/*/$@-*[0-9]*.rpm $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm; do rpmsign -v --addsign $$f || exit 1; done
	ls $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm > file.txt
	rsync --progress -av `cat file.txt` openresty.org:/home/agentz/www/misc/nginx/
	rsync --progress -av `cat file.txt` ~/packaging/SRPMS/
	cd ~/rpmbuild/RPMS && ./sync-repo
	cd ~/pkg/oss && ./build-repo
	#cd ~/pkg/oss && ./upload
	echo https://openresty.org/download/`basename $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm`
	curl -I https://openresty.org/download/`basename $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm`

.PHONY: $(priv_targets)
$(priv_targets):
	#echo $(rpmbuild_dir)
	if [ $@ = "lua-kafka-nginx-module-1.21.4" ]; then sed 's/NGINX_VERSION/1.21.4/' lua-kafka-nginx-module.spec | sed 's/OPENRESTY_VERSION/1.21.4.3/' > lua-kafka-nginx-module-1.21.4.spec; fi
	if [ $@ = "lua-kafka-nginx-module-1.25.3" ]; then sed 's/NGINX_VERSION/1.25.3/' lua-kafka-nginx-module.spec | sed 's/OPENRESTY_VERSION/1.25.3.1/' > lua-kafka-nginx-module-1.25.3.spec; fi
	echo $$PATH
	rm -f ~/rpmbuild/SRPMS/*.rpm ~/rpmbuild/RPMS/*/*.rpm
	spectool -g -R $@.spec
	sudo dnf builddep -y $@.spec
	echo -n|setsid time rpmbuild -v -ba $@.spec
	ls -lh $(rpmbuild_dir)/SRPMS/$@*[0-9]*.src.rpm
	mkdir -p ~/packaging/SRPMS/
	rsync --progress -av $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm ~/packaging/SRPMS/
	for f in $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm; do rpmsign -v --addsign $$f || exit 1; done
	for f in $(rpmbuild_dir)/RPMS/*/$@-*[0-9]*.rpm; do rpmsign -v --addsign $$f || exit 1; done
	ls -lh $(rpmbuild_dir)/RPMS/*/$@*[0-9]*.rpm
	rsync -av $(rpmbuild_dir)/RPMS/*/$@*[0-9]*.rpm ~/pkg/priv/`uname -m`/
	cd ~/pkg/priv && ./build-repo
	sudo dnf clean expire-cache
