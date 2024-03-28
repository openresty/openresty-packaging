Name:           openresty-util-linux
Version:        2.35.1.4
Release:        4%{?dist}
Summary:        OpenResty's fork of util-linux
Group:          System Environment/Base
License:        GPLv2 and GPLv2+ and LGPLv2+ and BSD with advertising and Public Domain
URL:            https://github.com/karelzak/util-linux

Source0:        util-linux-%{version}.tar.gz

AutoReqProv: no

%define util_linux_prefix %{_usr}/local/%{name}


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gettext-devel
BuildRequires: libselinux-devel
BuildRequires: ncurses-devel
BuildRequires: pkgconfig

%description
OpenResty's fork of util-linux for script and scriptreplay tools.

# ------------------------------------------------------------------------


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/util-linux-%{version}"; \
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
%setup -q -n util-linux-%{version}


%build

./configure \
    --prefix=/usr/local/openresty-util-linux \
    --libdir=/usr/local/openresty-util-linux/lib \
    --disable-libuuid --disable-libblkid \
    --disable-libmount --disable-libfdisk \
    --disable-fdisks --disable-mount --disable-losetup \
    --disable-zramctl --disable-fsck --disable-partx \
    --disable-uuidd --disable-mountpoint --disable-fallocate \
    --disable-setpriv \
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

make script scriptreplay dmesg prlimit \
    unshare nsenter \
    -j`nproc` > /dev/null


%install

make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/usr/share
rm -rf %{buildroot}/%{util_linux_prefix}/share
rm -rf %{buildroot}/%{util_linux_prefix}/lib/*.a
rm -rf %{buildroot}/%{util_linux_prefix}/lib/*.la
rm -rf %{buildroot}/%{util_linux_prefix}/lib/pkgconfig
rm -rf %{buildroot}/%{util_linux_prefix}/include
rm -rf %{buildroot}/%{util_linux_prefix}/sbin

mkdir -p %{buildroot}/%{util_linux_prefix}/bin_tmp
bin_dir=%{buildroot}/%{util_linux_prefix}/bin

# only copy commands we need
mv $bin_dir/script $bin_dir/scriptreplay \
    $bin_dir/dmesg $bin_dir/prlimit \
    $bin_dir/unshare $bin_dir/nsenter \
    %{buildroot}/%{util_linux_prefix}/bin_tmp/

rm -rf $bin_dir
mv %{buildroot}/%{util_linux_prefix}/bin_tmp $bin_dir


%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%dir %{util_linux_prefix}
%dir %{util_linux_prefix}/bin
%dir %{util_linux_prefix}/lib
%{util_linux_prefix}/bin/script
%defattr(-,root,root)
%{util_linux_prefix}/bin/script
%{util_linux_prefix}/bin/scriptreplay
%{util_linux_prefix}/bin/dmesg
%{util_linux_prefix}/bin/prlimit
%{util_linux_prefix}/bin/unshare
%{util_linux_prefix}/bin/nsenter
%{util_linux_prefix}/lib/*.so
%{util_linux_prefix}/lib/*.so.*
# ------------------------------------------------------------------------

%changelog
* Wed Feb 7 2024 Yichun Zhang (agentzh) 2.35.1.4-3
- upgraded openresty-util-linux to 2.35.1.4.
* Wed Feb 7 2024 Yichun Zhang (agentzh) 2.35.1.4-2
- upgraded openresty-util-linux to 2.35.1.4.
* Wed Feb 7 2024 Yichun Zhang (agentzh) 2.35.1.4-1
- upgraded openresty-util-linux to 2.35.1.4.
* Sun Feb 4 2024 Yichun Zhang (agentzh) 2.35.1.3-3
- upgraded openresty-util-linux to 2.35.1.3.
* Tue Nov 10 2020 Yichun Zhang (agentzh) 2.35.1.3-1
- upgraded openresty-util-linux to 2.35.1.3.
* Tue Aug 4 2020 Yichun Zhang (agentzh) 2.35.1.2-1
- upgraded openresty-util-linux to 2.35.1.2.
