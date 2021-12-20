Name:       openresty-docker
Version:    20.10.12
Release:    2%{?dist}
Source0:    https://github.com/moby/moby/archive/v%{version}.tar.gz
Source1:    docker.service
Source2:    docker.socket
Summary:    docker for OpenResty
Group:      Development/Libraries
License:    ASL 2.0
URL:        https://www.docker.com

Requires:   container-selinux
Requires:   libseccomp
Requires:   libcgroup
Requires:   containerd.io
Requires:   tar
Requires:   xz

# BuildRequires: cmake
# The most recent stable version of Go is required.
# BuildRequires: golang
BuildRequires: bash
BuildRequires: ca-certificates, gcc, git, glibc-static, make
BuildRequires: libtool, libtool-ltdl-devel
BuildRequires: pkgconfig
BuildRequires: tar
BuildRequires: device-mapper-devel
BuildRequires: libselinux-devel
BuildRequires: systemd-devel

AutoReq: no
AutoReqProv: no
AutoProv: no

%define docker_alias  moby
%define prefix        /usr/local/openresty-docker
%define go_build_dir  ${RPM_BUILD_DIR}/%{docker_alias}-%{version}/gobuild

%description
Docker is a product for you to build, ship and run any application as a
lightweight container.

Docker containers are both hardware-agnostic and platform-agnostic. This means
they can run anywhere, from your laptop to the largest cloud compute instance and
everything in between - and they don't require you to use a particular
language, framework or packaging system. That makes them great building blocks
for deploying and scaling web apps, databases, and backend services without
depending on a particular stack or provider.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{docker_alias}-%{version}"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%endif

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%if 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%prep
chmod u+w -R %{go_build_dir} || true # avoid permissing denied here
%setup -q -n "%{docker_alias}-%{version}" -a 0

%build

# disable btrfs support here
export DOCKER_BUILDTAGS='exclude_graphdriver_btrfs'
export PATH=/opt/go/bin:$PATH
export GOROOT=/opt/go
export GO111MODULE=off
export DOCKER_GITCOMMIT="v%{version}"
mkdir -p %{go_build_dir}/src/github.com/docker
ln -sf ${RPM_BUILD_DIR}/%{docker_alias}-%{version} %{go_build_dir}/src/github.com/docker/docker

pushd ${RPM_BUILD_DIR}/%{docker_alias}-%{version}
for component in tini "proxy dynamic";do
    TMP_GOPATH="%{go_build_dir}" PREFIX="%{go_build_dir}" hack/dockerfile/install/install.sh $component
done
GOPATH="%{go_build_dir}" VERSION=%{version} PRODUCT=docker hack/make.sh dynbinary
popd

%install
# install daemon binary
install -D -p -m 0755 $(readlink -f bundles/dynbinary-daemon/dockerd) ${RPM_BUILD_ROOT}%{prefix}/bin/dockerd

# install proxy
install -D -p -m 0755 %{go_build_dir}/docker-proxy ${RPM_BUILD_ROOT}%{prefix}/bin/docker-proxy

# install tini
install -D -p -m 755 %{go_build_dir}/docker-init ${RPM_BUILD_ROOT}%{prefix}/bin/docker-init

# install systemd scripts
install -D -m 0644 ${RPM_SOURCE_DIR}/docker.service ${RPM_BUILD_ROOT}/lib/systemd/system/openresty-docker.service
install -D -m 0644 ${RPM_SOURCE_DIR}/docker.socket ${RPM_BUILD_ROOT}/lib/systemd/system/openresty-docker.socket

%files
%{prefix}/bin/dockerd
%{prefix}/bin/docker-proxy
%{prefix}/bin/docker-init
/lib/systemd/system/openresty-docker.service
/lib/systemd/system/openresty-docker.socket

%post
if ! getent group docker > /dev/null; then
    groupadd --system docker
fi

%changelog
* Thu Dec 16 2021 Jiahao Wang - 20.10.12-1
- upgraded docker to 20.10.12.
* Tue Dec 14 2021 Jiahao Wang - 20.10.11-1
- initial build for openresty-docker.
