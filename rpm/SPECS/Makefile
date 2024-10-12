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
	  openresty-openssl3 \
	  openresty-openssl3-asan \
	  openresty-openssl3-debug \
	  openresty-pcre \
	  openresty-pcre2 \
	  openresty-pcre-asan \
	  openresty-pcre2-asan \
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

.PHONY: all
all: openresty

.PHONY: $(targets)
$(targets):
	#echo $(rpmbuild_dir)
	dnf makecache --disablerepo="*" --enablerepo="openresty" || true
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
