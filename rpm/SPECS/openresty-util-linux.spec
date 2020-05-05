Name:           openresty-util-linux
Version:        2.35.1.1
Release:        1%{?dist}
Summary:        OpenResty's fork of util-linux
Group:          System Environment/Base
License:        GPLv2 and GPLv2+ and LGPLv2+ and BSD with advertising and Public Domain
URL:            https://github.com/karelzak/util-linux

Source0:        util-linux-%{version}.tar.gz

AutoReqProv: no

%define util_linux_prefix %{_usr}/local/%{name}

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/util-linux-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gettext-devel
BuildRequires: libselinux-devel
BuildRequires: ncurses-devel
BuildRequires: pkgconfig

%description
OpenResty's fork of util-linux for script and scriptreplay tools.

# ------------------------------------------------------------------------

%prep
%setup -q -n util-linux-%{version}


%build

./configure \
    --prefix=%{util_linux_prefix} --disable-libuuid --disable-libblkid \
    --disable-libmount --disable-libsmartcols --disable-libfdisk\
    --disable-fdisks --disable-mount --disable-losetup \
    --disable-zramctl --disable-fsck --disable-partx \
    --disable-uuidd --disable-mountpoint --disable-fallocate \
    --disable-unshare --disable-nsenter --disable-setpriv \
    --disable-eject --disable-agetty --disable-cramfs \
    --disable-bfs --disable-minix --disable-fdformat \
    --disable-hwclock --disable-wdctl --disable-cal \
    --disable-logger --without-python --disable-pylibmount \
    --disable-lslogins --disable-switch_root --disable-pivot_root \
    --disable-lsmem --disable-chmem --disable-ipcrm \
    --disable-ipcs --disable-rfkill --disable-kill \
    --disable-last --disable-utmpdump --disable-mesg \
    --disable-raw --disable-rename --disable-login \
    --disable-nologin --disable-sulogin --disable-su \
    --disable-runuser --disable-ul --disable-more \
    --disable-setterm --disable-schedutils --disable-wall \
    --disable-irqtop --disable-lsirq

make script scriptreplay dmesg %{?_smp_mflags} > /dev/null


%install

# only need script and scriptreplay tools
mkdir -p %{buildroot}%{util_linux_prefix}/bin/
mv ./script ./scriptreplay ./dmesg %{buildroot}%{util_linux_prefix}/bin/


%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%defattr(-,root,root)
%{util_linux_prefix}/bin/script
%{util_linux_prefix}/bin/scriptreplay
%{util_linux_prefix}/bin/dmesg

# ------------------------------------------------------------------------

%changelog
