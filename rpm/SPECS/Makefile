rpmbuild_dir := $(shell ls -d $$HOME/rpmbuild)

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

priv_targets = openresty-plus \
		openresty-plus-debug \
		openresty-plus-test \
		openresty-plus-valgrind \
		openresty-plus-asan \
		openresty-plus-openssl \
		openresty-plus-openssl-debug \
		openresty-plus-openssl-asan \
		openresty-plus-openssl111 \
		openresty-plus-openssl111-debug \
		openresty-plus-openssl111-asan \
		openresty-gdb \
		openresty-python3 \
		openresty-stap \
		openresty-plus-hyperscan \
		openresty-postgresql \
		openresty-postgresql12 \
		openresty-elfutils \
		openresty-yajl \
		openresty-util-linux \
		openresty-postgresql-ip4r \
		openresty-postgresql12-ip4r \
		openresty-postgresql-orsl \
		openresty-postgresql12-orsl \
		openresty-postgresql12-timescaledb \
		openresty-postgresql-timescaledb \
		openresty-saas-zlib \
		openresty-saas-pcre \
		openresty-saas-openssl \
		openresty-saas-openssl111 \
		openresty-saas \
		openresty-binutils \
		openresty-tar \
		openresty-plzip \
		openresty-utils \
		openresty-firejail \
		openresty-odb \
		openresty-odb-debug \
		openresty-python3-cython \
		openresty-python3-setuptools \
		openresty-python3-numpy \
		openresty-python3-goto \
		openresty-maxminddb \
		openresty-maxminddb-debug \
		lua-resty-jsonb \
		openresty-pcap \
		openresty-tcpdump \
		openresty-coreutils \
		openresty-python3-xray-stats \
		openresty-nodejs \
		openresty-perl \
		openresty-perl-B-Flags \
		openresty-perl-ExtUtils-Config \
		openresty-perl-ExtUtils-Helpers \
		openresty-perl-ExtUtils-InstallPaths \
		openresty-perl-Module-Build-Tiny \
		openresty-perl-Readonly \
		openresty-perl-IPC-Run \
		openresty-perl-Opcodes \
		openresty-perl-IO-Tty \
		openresty-perl-B-C \
		openresty-keepalived \
		openresty-maxminddb-asan \
		openresty-maxminddb-utils \
		openresty-libbpf \
		openresty-perl-common-sense \
		openresty-perl-Canary-Stability \
		openresty-perl-Types-Serialiser \
        openresty-perl-JSON-XS \
		openresty-perl-App-cpanminus \
		openresty-perl-Net-SSLeay \
		openresty-perl-Mozilla-CA \
		openresty-perl-MIME-Base64 \
		openresty-perl-IO-Socket-SSL \
		openresty-perl-Protocol-WebSocket \
		openresty-plus-core \
		openresty-plus-core-h3 \
		openresty-edge-pki \
		openresty-libinjection \
		openresty-boringssl


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
	cd ~/rpmbuild/RPMS && ./sync-repo
	cd ~/pkg/oss && ./build-repo
	#cd ~/pkg/oss && ./upload
	echo https://openresty.org/download/`basename $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm`
	curl -I https://openresty.org/download/`basename $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm`

.PHONY: $(priv_targets)
$(priv_targets):
	#echo $(rpmbuild_dir)
	echo $$PATH
	rm -f ~/rpmbuild/SRPMS/*.rpm ~/rpmbuild/RPMS/*/*.rpm
	spectool -g -R $@.spec
	sudo dnf builddep -y $@.spec
	echo -n|setsid time rpmbuild -v -ba $@.spec
	for f in $(rpmbuild_dir)/RPMS/*/$@-*[0-9]*.rpm $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm; do rpmsign -v --addsign $$f || exit 1; done
	ls -lh $(rpmbuild_dir)/SRPMS/$@*[0-9]*.src.rpm
	mkdir -p ~/packaging/SRPMS/
	rsync --progress -av $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm ~/packaging/SRPMS/
	ls -lh $(rpmbuild_dir)/RPMS/*/$@*[0-9]*.rpm
	scp -v $(rpmbuild_dir)/RPMS/*/$@*[0-9]*.rpm ~/pkg/priv/x86_64/
	cd ~/pkg/priv && ./build-repo
	sudo dnf clean expire-cache
