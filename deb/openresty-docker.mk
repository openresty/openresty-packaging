## Author: spec2deb.pl
### Version: 0.01

OPENRESTY_DOCKER_VER := 20.10.12
WITHOUT_BTRFS=0

ifeq ($(DISTRO),jessie)
WITHOUT_BTRFS=1
endif
ifeq ($(DISTRO),stretch)
WITHOUT_BTRFS=1
endif
ifeq ($(DISTRO),trusty)
WITHOUT_BTRFS=1
endif
ifeq ($(DISTRO),xenial)
WITHOUT_BTRFS=1
endif
ifeq ($(DISTRO),bionic)
WITHOUT_BTRFS=1
endif

.PHONY: openresty-docker-download
openresty-docker-download:
	wget -nH --cut-dirs=100 --mirror 'https://github.com/moby/moby/archive/v$(OPENRESTY_DOCKER_VER).tar.gz'
	rm -rf openresty-docker_$(OPENRESTY_DOCKER_VER)
	mkdir -p openresty-docker_$(OPENRESTY_DOCKER_VER)
	tar -xf v$(OPENRESTY_DOCKER_VER).tar.gz --strip-components=1 -C openresty-docker_$(OPENRESTY_DOCKER_VER)
	tar -czf openresty-docker_$(OPENRESTY_DOCKER_VER).orig.tar.gz openresty-docker_$(OPENRESTY_DOCKER_VER)

openresty-docker-clean:
	-cd openresty-docker && debclean
	-find openresty-docker -maxdepth 1 ! -name 'debian' ! -name 'openresty-docker' -print | xargs rm -rf
	rm -rf openresty-docker*.deb
	rm -rf openresty-docker_*.*

.PHONY: openresty-docker-build
openresty-docker-build: openresty-docker-clean openresty-docker-download
	sudo apt-get -y -q install bash ca-certificates gcc git make libtool libltdl-dev pkg-config tar libdevmapper-dev libudev-dev
	sudo apt-get -y -q install --only-upgrade bash ca-certificates gcc git make libtool libltdl-dev pkg-config tar libdevmapper-dev libudev-dev
ifneq ($(WITHOUT_BTRFS),1)
	sudo apt-get -y -q install libbtrfs-dev
	sudo apt-get -y -q install --only-upgrade libbtrfs-dev
endif
	rm -f *.deb *.debian.tar.xz *.dsc *.changes
	tar xf openresty-docker_$(OPENRESTY_DOCKER_VER).orig.tar.gz --strip-components=1 -C openresty-docker
	cd openresty-docker \
		&& tpage --define distro=$(DISTRO) debian/changelog.tt2 > debian/changelog \
		&& tpage --define WITHOUT_BTRFS=$(WITHOUT_BTRFS) debian/control.tt2 \
			> debian/control \
		&& tpage --define WITHOUT_BTRFS=$(WITHOUT_BTRFS) debian/rules.tt2 \
			> debian/rules \
		&& debuild $(OPTS) -j$(JOBS)
	#if [ -f ./upload ]; then ./upload || exit 1; fi
