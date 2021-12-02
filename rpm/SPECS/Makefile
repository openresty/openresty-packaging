rpmbuild_dir := $(shell ls -d $$HOME/rpmbuild)

targets = openresty \
	  openresty-debug \
	  openresty-valgrind \
	  openresty-asan \
	  openresty-openssl \
	  openresty-openssl-debug \
	  openresty-openssl-asan \
	  openresty-pcre \
	  openresty-pcre-asan \
	  openresty-zlib \
	  openresty-zlib-asan \
	  perl-Test-Nginx \
	  perl-Lemplate \
	  perl-Test-LongString \
	  perl-Test-Base \
	  perl-Spiffy \
	  perl-Test-Deep

priv_targets = openresty-plus \
		openresty-plus-debug \
		openresty-plus-valgrind \
		openresty-plus-asan \
		openresty-plus-openssl \
		openresty-plus-openssl-debug \
		openresty-plus-openssl-asan \
		openresty-gdb \
		openresty-python3 \
		openresty-stap \
		openresty-plus-hyperscan \
		openresty-postgresql \
		openresty-elfutils \
		openresty-yajl \
		openresty-util-linux \
		openresty-postgresql-ip4r \
		openresty-postgresql-orsl \
		openresty-saas \
		openresty-binutils \
		openresty-tar \
		openresty-plzip \
		openresty-utils \
		openresty-saas-pcre \
		openresty-saas-openssl111 \
		openresty-saas-zlib

.PHONY: all
all: openresty

.PHONY: $(targets)
$(targets):
	#echo $(rpmbuild_dir)
	rm -f ~/rpmbuild/SRPMS/$@-[0-9]*.rpm ~/rpmbuild/RPMS/*/$@*-[0-9].rpm
	spectool -g -R $@.spec
	sudo dnf builddep -y $@.spec
	time rpmbuild -v -ba $@.spec
	#time rpmbuild -bi --short-circuit $@.spec
	#-cp -v ~/rpmbuild/SRPMS/$@*.src.rpm ~/rpmbuild/RPMS/*/$@*.rpm /tmp/
	ls -lh $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm
	ls -lh $(rpmbuild_dir)/RPMS/*/$@-[0-9]*.rpm
	for f in $(rpmbuild_dir)/RPMS/*/$@-*[0-9]*.rpm $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm; do rpmsign -v --addsign $$f || exit 1; done
	ls $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm > file.txt
	rsync -crlvpt `cat file.txt` openresty.org:/home/agentz/www/misc/nginx/
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
	#time rpmbuild -bi --short-circuit $@.spec
	#-cp -v ~/rpmbuild/SRPMS/$@*.src.rpm ~/rpmbuild/RPMS/*/$@*.rpm /tmp/
	ls -lh $(rpmbuild_dir)/SRPMS/$@*[0-9]*.src.rpm
	rsync --progress -av $(rpmbuild_dir)/SRPMS/$@-[0-9]*.src.rpm nuc:~/packaging/SRPMS/
	ls -lh $(rpmbuild_dir)/RPMS/*/$@*[0-9]*.rpm
	scp -v $(rpmbuild_dir)/RPMS/*/$@*[0-9]*.rpm ~/pkg/priv/x86_64/
	cd ~/pkg/priv && ./build-repo
	sudo dnf clean expire-cache
