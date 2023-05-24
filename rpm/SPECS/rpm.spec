# build against xz?
%bcond_without xz
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb
# run internal testsuite?
%bcond_without check
# build with plugins?
%bcond_without plugins
# build with sanitizers?
%bcond_with sanitizer
# build with libarchive? (needed for rpm2archive)
%bcond_without libarchive
# build with libimaevm.so
%bcond_without libimaevm
# build with new db format
%bcond_with ndb
# build with zstd support?
%bcond_without zstd
# build with lmdb support?
%bcond_with lmdb

%define rpmhome /usr/lib/rpm

%global rpmver 4.14.2.1
#global snapver rc2
%global rel 3

%global srcver %{version}%{?snapver:-%{snapver}}
%global srcdir %{?snapver:testing}%{!?snapver:%{name}-%(echo %{version} | cut -d'.' -f1-2).x}

%define bdbname libdb
%define bdbver 5.3.15
%define dbprefix db

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release: %{?snapver:0.%{snapver}.}%{rel}%{?dist}
Group: System Environment/Base
Url: http://www.rpm.org/
Source0: http://ftp.rpm.org/releases/%{srcdir}/%{name}-%{srcver}.tar.bz2
%if %{with int_bdb}
Source1: db-%{bdbver}.tar.gz
%else
BuildRequires: libdb-devel
%endif

# Disable autoconf config.site processing (#962837)
Patch1: rpm-4.11.x-siteconfig.patch
# Fedora specspo is setup differently than what rpm expects, considering
# this as Fedora-specific patch for now
Patch2: rpm-4.13.0-fedora-specspo.patch
# In current Fedora, man-pages pkg owns all the localized man directories
Patch3: rpm-4.9.90-no-man-dirs.patch
# gnupg2 comes installed by default, avoid need to drag in gnupg too
Patch4: rpm-4.8.1-use-gpg2.patch
# Temporary band-aid for rpm2cpio whining on payload size mismatch (#1142949)
Patch5: rpm-4.12.0-rpm2cpio-hack.patch

# Downstream-only patch:
# Add envvar that will be present during RPM build
# - Part of a Fedora Change for F28:
# - "Avoid /usr/bin/python in RPM build"
# - https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build
Patch7: rpm-4.14.1-Add-envvar-that-will-be-present-during-RPM-build.patch

# Patches already upstream:
Patch101: 0001-rpmfc-push-name-epoch-version-release-macro-before-i.patch

# These are not yet upstream
Patch906: rpm-4.7.1-geode-i686.patch
# Probably to be upstreamed in slightly different form
Patch907: rpm-4.13.90-ldflags.patch
Patch908: Fix-bump-up-the-limit-of-signature-header-to-64MB.patch

# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD
License: GPLv2+

Requires: coreutils
%if %{without int_bdb}
# db recovery tools, rpmdb_util symlinks
Requires: %{_bindir}/%{dbprefix}_stat
%endif
Requires: popt%{_isa} >= 1.10.2.1
Requires: curl

%if %{without int_bdb}
BuildRequires: %{bdbname}-devel
%endif

%if %{with check}
BuildRequires: fakechroot gnupg2
%endif

# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
BuildRequires: redhat-rpm-config
BuildRequires: gcc make
BuildRequires: gawk
BuildRequires: elfutils-devel >= 0.112
BuildRequires: elfutils-libelf-devel
BuildRequires: readline-devel zlib-devel
BuildRequires: openssl-devel
# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: gettext-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
BuildRequires: lua-devel >= 5.1
BuildRequires: libcap-devel
BuildRequires: libacl-devel
%if %{with xz}
BuildRequires: xz-devel >= 4.999.8
%endif
%if %{with libarchive}
BuildRequires: libarchive-devel
%endif
%if %{with zstd}
BuildRequires: libzstd-devel
%endif
%if %{with lmdb}
BuildRequires: lmdb-devel
%endif
# Only required by sepdebugcrcfix patch
BuildRequires: binutils-devel
# Couple of patches change makefiles so, require for now...
BuildRequires: automake libtool

%if %{with plugins}
BuildRequires: libselinux-devel
BuildRequires: dbus-devel
%endif

%if %{with sanitizer}
BuildRequires: libasan
BuildRequires: libubsan
#BuildRequires: liblsan
#BuildRequires: libtsan
%global sanitizer_flags -fsanitize=address -fsanitize=undefined
%endif

%if %{with libimaevm}
%if 0%{?fedora} >= 28 || 0%{?rhel} > 7
%global imadevname ima-evm-utils-devel
%else
%global imadevname ima-evm-utils
%endif
BuildRequires: %{imadevname} >= 1.0
%endif

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: %{name} = %{version}-%{release}
# librpm uses cap_compare, introduced sometimes between libcap 2.10 and 2.16.
# A manual require is needed, see #505596
Requires: libcap%{_isa} >= 2.16
# Drag in SELinux support at least for transition phase
%if %{with plugins} && 0%{?fedora} >= 28
Requires: rpm-plugin-selinux%{_isa} = %{version}-%{release}
%endif
# Remove temporary compat-librpm3 package from F23
Obsoletes: compat-librpm3 < %{version}-%{release}

%description libs
This package contains the RPM shared libraries.

%package build-libs
Summary:  Libraries for building RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description build-libs
This package contains the RPM shared libraries for building packages.

%package sign-libs
Summary:  Libraries for signing RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm-libs%{_isa} = %{version}-%{release}
Requires: %{_bindir}/gpg2

%description sign-libs
This package contains the RPM shared libraries for signing packages.

%package devel
Summary:  Development files for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{_isa} = %{version}-%{release}
Requires: %{name}-build-libs%{_isa} = %{version}-%{release}
Requires: %{name}-sign-libs%{_isa} = %{version}-%{release}
Requires: popt-devel%{_isa}

%description devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary: Scripts and executable programs used to build packages
Group: Development/Tools
Requires: rpm = %{version}-%{release}
Requires: elfutils >= 0.128 binutils
Requires: findutils sed grep gawk diffutils file patch >= 2.5
Requires: tar unzip gzip bzip2 cpio xz zstd
Requires: pkgconfig >= 1:0.24
Requires: /usr/bin/gdb-add-index
# Technically rpmbuild doesn't require any external configuration, but
# creating distro-compatible packages does. To make the common case
# "just work" while allowing for alternatives, depend on a virtual
# provide, typically coming from redhat-rpm-config.
Requires: system-rpm-config

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package sign
Summary: Package signing support
Group: System Environment/Base
Requires: rpm-sign-libs%{_isa} = %{version}-%{release}

%description sign
This package contains support for digitally signing RPM packages.

%package -n python2-%{name}
Summary: Python 2 bindings for apps which will manipulate RPM packages
Group: Development/Libraries
BuildRequires: python2-devel
%{?python_provide:%python_provide python2-%{name}}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}-python = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}

%description -n python2-%{name}
The python2-rpm package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 2
programs that will manipulate RPM packages and databases.

%package -n python3-%{name}
Summary: Python 3 bindings for apps which will manipulate RPM packages
Group: Development/Libraries
BuildRequires: python3-devel
%{?python_provide:%python_provide python3-%{name}}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}
Obsoletes: platform-python-%{name} < %{version}-%{release}

%description -n python3-%{name}
The python3-rpm package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 3
programs that will manipulate RPM packages and databases.

%package apidocs
Summary: API documentation for RPM libraries
Group: Documentation
BuildArch: noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%package cron
Summary: Create daily logs of installed packages.
Group: System Environment/Base
BuildArch: noarch
Requires: crontabs logrotate rpm = %{version}-%{release}

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.

%if %{with plugins}
%package plugin-selinux
Summary: Rpm plugin for SELinux functionality
Group: System Environment/Base
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-selinux
%{summary}

%package plugin-syslog
Summary: Rpm plugin for syslog functionality
Group: System Environment/Base
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-syslog
%{summary}

%package plugin-systemd-inhibit
Summary: Rpm plugin for systemd inhibit functionality
Group: System Environment/Base
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-systemd-inhibit
This plugin blocks systemd from entering idle, sleep or shutdown while an rpm
transaction is running using the systemd-inhibit mechanism.

%package plugin-ima
Summary: Rpm plugin ima file signatures
Group: System Environment/Base
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-ima
%{summary}

%package plugin-prioreset
Summary: Rpm plugin for resetting scriptlet priorities for SysV init
Group: System Environment/Base
Requires: rpm-libs%{_isa} = %{version}-%{release}

%description plugin-prioreset
%{summary}

Useful on legacy SysV init systems if you run rpm transactions with
nice/ionice priorities. Should not be used on systemd systems.

%endif # with plugins

%prep
%autosetup -n %{name}-%{srcver} %{?with_int_bdb:-a 1} -p1

%if %{with int_bdb}
ln -s db-%{bdbver} db
%endif

# Python madness: invoke python2 explicitly to avoid deprecation warnings
# breaking the testsuite and thus the build. Easier than managing a patch...
sed -ie 's:^python test:python2 test:g' tests/rpmtests tests/local.at

%build
%if %{without int_bdb}
#CPPFLAGS=-I%{_includedir}/db%{bdbver}
#LDFLAGS=-L%{_libdir}/db%{bdbver}
%endif
CPPFLAGS="$CPPFLAGS -DLUA_COMPAT_APIINTCASTS"
CFLAGS="$RPM_OPT_FLAGS %{?sanitizer_flags} -DLUA_COMPAT_APIINTCASTS"
LDFLAGS="$LDFLAGS %{?__global_ldflags}"
export CPPFLAGS CFLAGS LDFLAGS

autoreconf -i -f

# Hardening hack taken from macro %%configure defined in redhat-rpm-config
for i in $(find . -name ltmain.sh) ; do
     %{__sed} -i.backup -e 's~compiler_flags=$~compiler_flags="%{_hardened_ldflags}"~' $i
done;

# Using configure macro has some unwanted side-effects on rpm platform
# setup, use the old-fashioned way for now only defining minimal paths.
./configure \
    --prefix=%{_usr} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_var} \
    --sharedstatedir=%{_var}/lib \
    --libdir=%{_libdir} \
    --build=%{_target_platform} \
    --host=%{_target_platform} \
    --with-vendor=redhat \
    %{!?with_int_bdb: --with-external-db} \
    %{!?with_plugins: --disable-plugins} \
    --with-lua \
    --with-selinux \
    --with-cap \
    --with-acl \
    %{?with_ndb: --with-ndb} \
    %{?with_libimaevm: --with-imaevm} \
    %{?with_zstd: --enable-zstd} \
    %{?with_lmdb: --enable-lmdb} \
    --enable-python \
    --with-crypto=openssl

make %{?_smp_mflags}

pushd python
%{__python2} setup.py build
%{__python3} setup.py build
popd

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

# We need to build with --enable-python for the self-test suite, but we
# actually package the bindings built with setup.py (#531543#c26)
pushd python
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd


# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/tmpfiles.d
echo "r /var/lib/rpm/__db.*" > ${RPM_BUILD_ROOT}/usr/lib/tmpfiles.d/rpm.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
mkdir -p $RPM_BUILD_ROOT%{rpmhome}/macros.d

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Obsoletename \
    Packages Providename Requirename Triggername Sha1header Sigmd5 \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

# plant links to relevant db utils as rpmdb_foo for documention compatibility
%if %{without int_bdb}
for dbutil in dump load recover stat upgrade verify
do
    ln -s ../../bin/%{dbprefix}_${dbutil} $RPM_BUILD_ROOT/%{rpmhome}/rpmdb_${dbutil}
done
%endif

%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.la"|xargs rm -f

# These live in perl-generators and python-rpm-generators now
rm -f $RPM_BUILD_ROOT/%{rpmhome}/{perldeps.pl,perl.*,pythond*}
rm -f $RPM_BUILD_ROOT/%{_fileattrsdir}/{perl*,python*}
# Axe unused cruft
rm -f $RPM_BUILD_ROOT/%{rpmhome}/{tcl.req,osgideps.pl}

# Avoid unnecessary dependency on /usr/bin/python
chmod a-x $RPM_BUILD_ROOT/%{rpmhome}/python-macro-helper

%if %{with check}
%check
make check || cat tests/rpmtests.log
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post build-libs -p /sbin/ldconfig
%postun build-libs -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%doc CREDITS doc/manual/[a-z]*

/usr/lib/tmpfiles.d/rpm.conf
%dir %{_sysconfdir}/rpm

%attr(0755, root, root) %dir /var/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/rpm/*

%{_bindir}/rpm
%{_bindir}/rpm2archive
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpm-misc.8*

# XXX this places translated manuals to wrong package wrt eg rpmbuild
%lang(fr) %{_mandir}/fr/man[18]/*.[18]*
%lang(ko) %{_mandir}/ko/man[18]/*.[18]*
%lang(ja) %{_mandir}/ja/man[18]/*.[18]*
%lang(pl) %{_mandir}/pl/man[18]/*.[18]*
%lang(ru) %{_mandir}/ru/man[18]/*.[18]*
%lang(sk) %{_mandir}/sk/man[18]/*.[18]*

%attr(0755, root, root) %dir %{rpmhome}
%{rpmhome}/lua
%{rpmhome}/macros
%{rpmhome}/macros.d
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc

%{rpmhome}/rpmdb_*
%{rpmhome}/rpm.daily
%{rpmhome}/rpm.log
%{rpmhome}/rpm.supp
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg

%{rpmhome}/platform

%dir %{rpmhome}/fileattrs

%files libs
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%if %{with plugins}
%dir %{_libdir}/rpm-plugins

%files plugin-syslog
%{_libdir}/rpm-plugins/syslog.so

%files plugin-selinux
%{_libdir}/rpm-plugins/selinux.so

%files plugin-systemd-inhibit
%{_libdir}/rpm-plugins/systemd_inhibit.so
%{_mandir}/man8/rpm-plugin-systemd-inhibit.8*

%files plugin-ima
%{_libdir}/rpm-plugins/ima.so

%files plugin-prioreset
%{_libdir}/rpm-plugins/prioreset.so
%endif # with plugins

%files build-libs
%{_libdir}/librpmbuild.so.*

%files sign-libs
%{_libdir}/librpmsign.so.*

%files build
%{_bindir}/rpmbuild
%{_bindir}/gendiff
%{_bindir}/rpmspec

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*

%{rpmhome}/brp-*
%{rpmhome}/check-*
%{rpmhome}/debugedit
%{rpmhome}/sepdebugcrcfix
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/python-macro-helper
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/config.*
%{rpmhome}/mkinstalldirs
%{rpmhome}/macros.p*
%{rpmhome}/fileattrs/*

%files sign
%{_bindir}/rpmsign
%{_mandir}/man8/rpmsign.8*

%files -n python2-%{name}
%{python2_sitearch}/%{name}/
%{python2_sitearch}/%{name}-%{version}*.egg-info

%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}*.egg-info

%files devel
%{_mandir}/man8/rpmgraph.8*
%{_bindir}/rpmgraph
%{_libdir}/librp*[a-z].so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files cron
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm

%files apidocs
%license COPYING
%doc doc/librpm/html/*

%changelog
* Mon Oct 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.2.1-2
- Push name/epoch/version/release macro before invoking depgens

* Mon Oct 22 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2.1-1
- Update to rpm 4.14.2.1 (http://rpm.org/wiki/Releases/4.14.2.1)

* Wed Aug 22 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.2-1
- Update to rpm 4.14.2 (http://rpm.org/wiki/Releases/4.14.2)

* Tue May 22 2018 Mark Wielaard <mjw@fedoraproject.org> - 4.14.1-9
- find-debuginfo.sh: Handle application/x-pie-executable (#1581224)

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.1-8
- Split rpm-build-libs to one more subpackage rpm-sign-libs

* Mon Feb 19 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-7
- Explicitly BuildRequire gcc and make

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.1-6.1
- Escape macros in %%changelog

* Wed Jan 31 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-6
- Avoid unnecessary macro helper dependency on /usr/bin/python (#1538657)
- Fix release of previous changelog entry

* Tue Jan 30 2018 Tomas Orsava <torsava@redhat.com> - 4.14.1-5
- Add envvar that will be present during RPM build,
  Part of a Fedora Change for F28: "Avoid /usr/bin/python in RPM build"
  https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build

* Tue Jan 30 2018 Petr Viktorin <pviktori@redhat.com> - 4.14.1-4
- Skip automatic Python byte-compilation if *.py files are not present

* Thu Jan 25 2018 Florian Weimer <fweimer@redhat.com> - 4.14.1-3
- Rebuild to work around gcc bug leading to librpm miscompilation (#1538648)

* Thu Jan 18 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-2
- Avoid nuking the new python-macro-helper along with dep generators (#1535692)

* Tue Jan 16 2018 Panu Matilainen <pmatilai@redhat.com> - 4.14.1-1
- Rebase to rpm 4.14.1 (http://rpm.org/wiki/Releases/4.14.1)

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.0-5
- Fix typo in Obsoletes

* Mon Nov 06 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.14.0-4
- Remove platform-python bits

* Thu Oct 26 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-3
- Move selinux plugin dependency to selinux-policy in Fedora >= 28 (#1493267)

* Thu Oct 12 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-2
- Dump out test-suite log in case of failures again
- Don't assume per-user groups in test-suite

* Thu Oct 12 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-1
- Rebase to rpm 4.14.0 final (http://rpm.org/wiki/Releases/4.14.0)

* Tue Oct 10 2017 Troy Dawson <tdawson@redhat.com> - 4.14.0-0.rc2.6
- Cleanup spec file conditionals

* Tue Oct 03 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.5
- Add build conditionals for zstd and lmdb support
- Enable zstd support

* Tue Oct 03 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.4
- Spec cleanups

* Fri Sep 29 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.3
- BuildRequire gnupg2 for the testsuite

* Fri Sep 29 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.2
- ima-evm-utils only has a -devel package in fedora >= 28

* Thu Sep 28 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc2.1
- Rebase to rpm 4.14.0-rc2 (http://rpm.org/wiki/Releases/4.14.0)

* Mon Sep 18 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc1.3
- Fix Ftell() past 2GB on 32bit architectures (#1492587)

* Thu Sep 07 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc1.2
- Actually honor with/without libimaevm option
- ima-evm-utils-devel >= 1.0 is required for rpm >= 4.14.0

* Wed Sep 06 2017 Panu Matilainen <pmatilai@redhat.com> - 4.14.0-0.rc1.1
- Rebase to rpm 4.14.0-rc1 (http://rpm.org/wiki/Releases/4.14.0)
- Re-enable SHA256 header digest generation (see #1480407)

* Mon Aug 28 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.8
- Band-aid for DB_VERSION_MISMATCH errors on glibc updates (#1465809)

* Thu Aug 24 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.7
- Remove ugly kludges from posttrans script, BDB handles this now

* Fri Aug 18 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.6
- Silence harmless but bogus error message on noarch packages (#1482144)

* Thu Aug 17 2017 Miro Hrončok <mhroncok@redhat.com> - 4.13.90-0.git14002.5
- Build with platform_python

* Mon Aug 14 2017 Miro Hrončok <mhroncok@redhat.com> - 4.13.90-0.git14000.4
- Add platform-python bytecompilation patch: platform-python-bytecompile.patch
- Add platform python deps generator patch: platform-python-abi.patch
- Add a platform-python subpackage and remove system python related declarations
- Build rpm without platform_python for bytecompilation
  (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Mon Aug 14 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.3
- Disable macro argument quoting as a band-aid to #1481025

* Fri Aug 11 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.2
- Disable SHA256 header-only digest generation temporarily (#1480407)

* Thu Aug 10 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.90-0.git14000.1
- Rebase to rpm 4.13.90 aka 4.14.0-alpha (#1474836)

* Mon Jul 31 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-41
- Move _debuginfo_subpackages and _debugsource_packages to redhat-rpm-config

* Sat Jul 29 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-40
- Update latest patches from merged versions

* Fri Jul 28 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-39
- Backport fixes for debuginfo subpackages

* Wed Jul 26 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-38
- Backport trivial fix for debugsourcefiles.list ending up in random dir

* Tue Jul 25 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-37
- Enable debugsource and debuginfo subpackages by default

* Mon Jul 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-36
- Make sure that test results are not ignored

* Sun Jul 23 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-35
- Fix rpmfd_write on big endian arches.

* Fri Jul 21 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-34
- find-debuginfo.sh: Remove non-allocated NOBITS sections from minisymtab.

* Thu Jul 20 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-33
- Remove strict requirement on python libs

* Tue Jul 18 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-32
- Add find-debuginfo.sh: Add --keep-section and --remove-section (#1465997)

* Wed Jul 12 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-31
- Add automatic provides debuginfo(build-id) = ... into debuginfo subpackages

* Fri Jul 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.13.0.1-30
- Fix brokeness when using %%filter_setup (RHBZ #1468476)

* Tue Jul 04 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-29
- Track patches using https://pagure.io/rpm-fedora
- Use file list to explicitly set mode for build-id dirs/files
  (#1452893, #1458839)

* Thu Jun 29 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-28
- Add debugedit-prefix.patch.
- Add find-debuginfo-filter-built-ins.patch.
- Add find-debuginfo-dwz-multi.patch.
- Add find-debuginfo-and-macro-docs.patch.

* Wed Jun 28 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-27
- Add find-debuginfo-split-traversal-and-extraction-fix.patch (#1465170)

* Wed Jun 28 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.13.0.1-26
- Backport patches for rich dependencies from dependency generators

* Sun Jun 25 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-25
- Add support for debugsource and debuginfo subpackages
  - find-debuginfo-untangle-unique-build-options.patch
  - debugsrc-and-sub-debuginfo-packages.patch

* Fri Jun 23 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-24
- Backport parallel debuginfo processing.

* Tue May 30 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-23
- Fix resetting attr flags in buildid creation (#1449732)

* Tue May 23 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.0.1-22
- Python dependency generators live in python-rpm-generators now (#1444925)

* Tue May 23 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.0.1-21
- Fix rpmsign python module import failing (#1393659)

* Tue Apr 25 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-20
- Fix rpmbuild world writable empty (tmp) dirs in debuginfo (#641022)

* Sat Apr 15 2017 Mark Wielaard <mjw@fedoraproject.org> - 4.13.0.1-19
- Minisymtab should only be added for executables or shared libraries.
- Add find-debuginfo.sh -n (debugedit --no-recompute-build-id) option.

* Fri Mar 31 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.0.1-18
- gpg path must not depend on %%_prefix and such (#1437726)

* Mon Mar 27 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.0.1-17
- Work around missing python[23] during build dependency parse
- Include ISA in the new python library version dependencies too

* Mon Mar 27 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.0.1-16
- Band-aid for python library versioning inadequacies (#1435135)

* Mon Mar 27 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-15
- Unbreak short-circuited binary builds (#1434235).

* Tue Mar 21 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-14
- Add fix for off by one adding DW_FORM_string replacement (#1434347).

* Mon Mar 20 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-13
- Add tests fix for sed file build-id regexp matching.
- Add fix for build-ids in non-executable ELF files (#1433837).

* Fri Mar 17 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-12
- Fix reading and updating (cross-endian) build-id information.

* Fri Mar 17 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-11
- Do not process build-ids for noarch packages.

* Thu Mar 16 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-10
- Add fix for debugedit replace debug_line files.

* Thu Mar 16 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.13.0.1-9
- Switch to OpenSSL (RHBZ #1390624)

* Wed Mar 15 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-8
- Add fix to reset buildid file attributes (#1432372)

* Fri Mar 10 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-7
- Add fixup fix for build-id warnings on object files (#1430587)

* Thu Mar 09 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-6
- Add fix for missing_build_ids_terminate_build without __debug_package.

* Thu Mar 09 2017 Mark Wielaard <mjw@redhat.com> - 4.13.0.1-5
- Add fix for build-id warnings on object files (#1430587)

* Wed Mar 08 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.0.1-4
- Mark Wielaard's backports for debuginfo parallel installation etc (#1427970)

* Fri Feb 24 2017 Pavlina Moravcova Varekova <pmoravco@redhat.com> - 4.13.0.1-3
- Fix number of references on spec_Type (#1426578)

* Thu Feb 16 2017 Tomas Orsava <torsava@redhat.com> - 4.13.0.1-2
- Fix handling of Python wheels by pythondistdeps.py --provides (#1421776)

* Thu Feb 16 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.0.1-1
- Update to 4.13.0.1 ((http://rpm.org/wiki/Releases/4.13.0)

* Tue Feb 14 2017 Florian Festi <ffesti@rpm.org> - 4.13.0-12
- Fix Python byte compilation for Python3 only packages (#1411588)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.0-11.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Panu Matilainen <pmatilai@redhat.com> - 4.13.0-11
- Fix malformed packages being generated around 4GB boundary (#1405570)
- Resurrect debuginfo GDB index generation (#1410907)

* Fri Jan 06 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.13.0-10
- Add Requires: python-setuptools for rpm-build (RHBZ #1410631)

* Wed Dec 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 4.13.0-9
- Rebuild for Python 3.6

* Sun Dec 18 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.13.0-8
- Switch rpm-build to system-python (RHBZ #1405483)

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 4.13.0-7
- Rebuild for Python 3.6

* Sat Dec 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.13.0-6
- Fix arch-dependent requires in subpackages (RHBZ #1398591)

* Fri Nov 25 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.13.0-5
- Fix arch-dependent requires in subpackages (RHBZ #1398591)

* Fri Nov 11 2016 Panu Matilainen <pmatilai@redhat.com> - 4.13.0-4
- Expand python subpackage obsoletion range (related: #1394125)

* Mon Nov 07 2016 Panu Matilainen <pmatilai@redhat.com> - 4.13.0-3
- Fix invalid memory access on %%transfiletriggerpostun (#1284645)

* Fri Nov 04 2016 Thierry Vignaud <tvignaud@redhat.com> - 4.13.0-2
- Fix package name references in python sub-packages to match reality
- Re-enable test-suite now that it works again

* Thu Nov 03 2016 Panu Matilainen <pmatilai@redhat.com> - 4.13.0-1
- Rebase to rpm 4.13.0 final (http://rpm.org/wiki/Releases/4.13.0)

* Wed Nov 02 2016 Panu Matilainen <pmatilai@redhat.com> - 4.13.0-0.rc2.2
- Fix harmless unused variable warning from fedora-specspo patch

* Thu Oct 20 2016 Panu Matilainen <pmatilai@redhat.com> - 4.13.0-0.rc2.1
- Rebase to rpm 4.13.0-rc2

* Fri Sep 23 2016 Richard W.M. Jones <rjones@redhat.com> - 4.13.0-0.rc1.47
- Backport two upstream patches which add riscv64 architecture support.

* Wed Aug 24 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.13.0-0.rc1.46
- Backport patch for missing import in Python dependency generator

* Wed Aug 24 2016 Kalev Lember <klember@redhat.com> - 4.13.0-0.rc1.45
- Fix -python2 and -python3 subpackage obsoleting from .42

* Tue Aug 23 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.13.0-0.rc1.44
- Use %%python_provide for python3 subpackage

* Mon Aug 22 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.13.0-0.rc1.43
- Backport fixes to ignore .egg-link files in Python dependency  generator

* Fri Aug 12 2016 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.42
- Enable --majorver-provides in Python dependency generator

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 4.13.0-0.rc1.41
- Add %%{?system_python_abi}
- rpm-python -> python2-rpm && rpm-python3 -> python3-rpm with providing old names
- Fixes and cleanups

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.0-0.rc1.40.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 Petr Pisar <ppisar@redhat.com> - 4.13.0-0.rc1.40
- Drop rpm-build's dependency on perl-generators (bug #1158860)

* Fri Jul 15 2016 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.39
- Pass relevant files to new Python dependency generator

* Mon Jun 13 2016 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.38
- Add new Python dependency generator (provides only for now) (#1340885)

* Thu Jun 02 2016 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.37
- Add support for _buildhost macro (#1309367)

* Mon May 23 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.36
- Fix signing with non-ASCII uid keys (#1243963)

* Thu May 19 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.35
- Use armv7hl isa for all armhfp (armv7h*l) arches (#1326871)

* Tue May 17 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.34
- Filter unversioned deps if corresponding versioned deps exist (#678605)

* Mon Apr 25 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.33
- Fix sigsegv in stringFormat() (#1316903)
- Fix reading rpmtd behind its size in formatValue() (#1316896)

* Fri Apr 15 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.32
- escape %% chars in previous changelog record

* Fri Apr 15 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.31
- Enable --no-backup-if-mismatch by default in %%patch macro (#884755)
- Add %%{_default_patch_flags} to %%__patch which is used in %%autosetup
- Use fuzz settings for %%autopatch/%%autosetup

* Thu Apr 14 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0-rc1.30
- Make creating index records consistent for rich and rich-weak deps (#1325982)

* Tue Apr 12 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.29
- Add RPMCALLBACK_ELEM_PROGRESS callback type (needed by dnf)

* Wed Apr 06 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.28
- Fix non-working combination of %%lang and %%doc directive (#1254483)

* Thu Mar 10 2016 Lubos Kardos <lkardos@redhat.com> 4.13.0-0.rc1.27
- Add posix.redirect2null (#1287918)

* Fri Feb 26 2016 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.26
- Fix ExclusiveArch/ExcludeArch for noarch packages (#1298668)

* Thu Feb 25 2016 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.25
- Fix dependencies for RemovePathPostfixes (#1306559)

* Fri Feb 19 2016 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.24
- Also block idle and sleep in the systemd-inhibit plugin (#1297984)
- Add support for MIPS release 6
- Add mips32 mips64 mipsel and mipseb macros (#1285116)

* Tue Feb 02 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.23
- Remove size limit when expanding macros (#1301677)

* Mon Feb 01 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.22
- Harden rpm package again, previous attempt had to be reverted (#1289734)

* Mon Feb 01 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.21
- Remove setting %%_gnu macro explictly, no more needed (#1303265)

* Mon Feb 01 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.20
- Revert using %%configure, it causes problems
- Temporary set %%_gnu macro explictly, just for one build (#1303265)

* Fri Jan 29 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.19
- Use %%configure macro, harden rpm package (#1289734)

* Tue Jan 19 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.18
- Escape %%autosetup in previous changelog record

* Tue Jan 19 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.17
- Fix %%autosetup not to cause errors during run of rpmspec tool (#1293687)

* Fri Jan 15 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.16
- Fix recursive calling of rpmdeps tool (#1297557)

* Fri Jan 15 2016 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.15
- Add support for missingok file attribute

* Fri Jan 15 2016 Lubos Kardos <lkardos@redhat.com> - 4.13.0-0.rc1.14
- Fix not chrooting transaction file triggers

* Mon Nov 23 2015 Lubos Kardos <lkardos@rpm.org> - 4.13.0-0.rc1.13
- Add possibility to disable file triggers
- Fix unwanted multiple execution of filetriggers in dnf (#1282115)

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.0-0.rc1.12
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Nov 06 2015 Lubos Kardos <lkardos@rpm.org> - 4.13.0-0.rc1.11
- Fix crash when parsing corrupted RPM file (#1273360)

* Fri Nov 06 2015 Lubos Kardos <lkardos@rpm.org> - 4.13.0-0.rc1.10
- Fix SIGSEGV in case of old unsupported gpg keys (#1277464)

* Fri Oct 30 2015 Lubos Kardos <lkardos@rpm.org> - 4.13.0-0.rc1.9
- Ignore SIGPIPE signals during execucton of scriptlets (#1264198)

* Fri Oct 30 2015 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.8
- Move /usr/lib/rpm/fileattrs directory from rpm-build to rpm (#1272766)

* Fri Oct 23 2015 Lubos Kardos <lkardos@redhat.com> - 4.13-0.rc1.7
- Fix reading a memory right after the end of an allocated area (#1260248)
- Add support for various types of dependencies to rpmdeps tool (#1247092)
- fix %%autopatch when patch do not exist (#1244172)

* Fri Oct 23 2015 Lubos Kardos <lkardos@redhat.com> - 4.13-0.rc1.6
- If %%_wrong_version_format_terminate_build is 1 then terminate build in case
  that version format is wrong i. e. epoch is not unsigned integer or version
  contains more separators (":", "-"). %%_wrong_version_format_terminate_build
  is 1 by deafault (#1265700)

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 4.13.0-0.rc1.5
- Rebuilt for Python3.5 rebuild

* Mon Oct 12 2015 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.4
- Fix selinux plugin for permissive mode

* Mon Sep 07 2015 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.3
- Fix new rich dependency syntax

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 4.13.0-0.rc1.2
- Obsolete compat-librpm3

* Wed Sep 02 2015 Florian Festi <ffesti@rpm.org> - 4.13.0-0.rc1.1
- Update to upstream rc1 release

* Mon Aug 10 2015 Lubos Kardos <lkardos@redhat.com> - 4.12.90-7
- Fix last occurence of PyString

* Thu Aug 06 2015 Lubos Kardos <lkardos@redhat.com> - 4.12.90-6
- Add --filetriggers option to show info about file triggers.

* Mon Aug 03 2015 Lubos Kardos <lkardos@redhat.com> - 4.12.90-5
- If globbing of a filename fails, try use the filename without globbing.
  (#1246743)
- Modify rpmIsGlob() to be more precise and compatible with glob().
  (#1246743)

* Thu Jul 30 2015 Lubos Kardos <lkardos@redhat.com> - 4.12.90-4
- Don't warn when an escaped macro is in a comment (#1224660)

* Mon Jul 27 2015 Florian Festi <ffesti@rpm.org> - 4.12.90-3
- Fix compressed patches (#1247248)

* Mon Jul 27 2015 Lubos Kardos <lkardos@redhat.com> - 4.12.90-2
- Enable braces expansion in rpmGlob() (#1246743)

* Fri Jul 24 2015 Florian Festi <ffesti@rpm.org> - 4.12.90-1
- Update to upstream alpha release

* Tue Jul 14 2015 Michal Toman <mtoman@fedoraproject.org> - 4.12.0.1-18
- Add support for MIPS platform

* Mon Jun 29 2015 Florian Festi <ffesti@rpm.org> - 4.12.0.1-17
- Fix Python import directive for more strict Python3 search rules (#1236493)

* Fri Jun 19 2015 Lubos Kardos <lkardos@redhat.com> 4.12.0.1-16
- Allow gpg to get passphrase by itself (#1228234)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.12.0.1-15.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Florian Festi <ffesti@rpm.org> - 4.12.0.1-15
- Add --whatrecommends and friends (#1231247)

* Wed Apr 15 2015 Florian Festi <ffesti@rpm.org> - 4.12.0.1-14
- Fix references to sources in golang debuginfo packages (#1184221)

* Tue Mar 31 2015 Lubos Kardos <lkardos@redhat.com> 4.12.0-13
- Fix wrong use of variable strip_g in find-debuginfo.sh (#1207434)

* Mon Mar 30 2015 Lubos Kardos <lkardos@redhat.com> 4.12.0-12
- Fix segmentation fault (#1206750)

* Fri Mar 27 2015 Lubos Kardos <lkardos@redhat.com> 4.12.0-11
- Pass _find_debuginfo_opts -g to eu-strip for executables (#1186563)
- add_minidebug is not ran when strip_g is set (#1186563)

* Fri Mar 20 2015 Lubos Kardos <lkardos@redhat.com> 4.12.0-10
- Fix "--excludedocs" option (#1192625)

* Fri Mar 20 2015 Florian Festi <ffesti@rpm.org> - 4.12.0.1-9
- Fix spec to allow building without plugins (#1182385)

* Mon Mar 16 2015 Than Ngo <than@redhat.com> - 4.12.0.1-8
- bump release and rebuild so that koji-shadow can rebuild it
  against new gcc on secondary arch

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4.12.0.1-7.1
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 4.12.0.1-7
- Include upstream patch to fix find-debuginfo (http://www.rpm.org/ticket/887).

* Fri Jan 16 2015 Tom Callaway <spot@fedoraproject.org> - 4.12.0.1-6
- rebuild against lua 5.3

* Fri Dec 12 2014 Lubos Kardos <lkardos@redhat.com> - 4.12.0.1-5
- Add check against malicious CPIO file name size (#1168715)
- Fixes CVE-2014-8118
- Fix race condidition where unchecked data is exposed in the file system
  (#1039811)
- Fixes CVE-2013-6435

* Thu Oct 30 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0.1-4
- Axe unused generator scripts forcing a perl dependency (#1158580, #1158583)

* Tue Oct 28 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0.1-3
- Skip ghost files in payload (#1156497)
- Fix size and archice size tag generation on big-endian systems

* Wed Oct 01 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0.1-2
- Dont wait for transaction lock inside scriptlets (#1135596)

* Thu Sep 18 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0.1-1
- Update to rpm-4.12.0.1 final (http://rpm.org/wiki/Releases/4.12.0.1)
- Temporary workaround payload size mismatch issue in rpm2cpio (#1142949)

* Wed Sep 17 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-2
- Reduce the double separator spec parse error into a warning (#1065563)

* Tue Sep 16 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-1
- Update to rpm-4.12.0 final (http://rpm.org/wiki/Releases/4.12.0)

* Tue Sep 02 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-0.rc1.2
- Resurrect payload and tilde rpmlib() dependencies

* Wed Aug 27 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-0.rc1.1
- Update to rpm-4.12.0-rc1

* Mon Aug 25 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-0.beta1.6
- Resurrect dependency logging on package build
- Resurrect rpmlib() dependencies in src.rpms

* Wed Aug 20 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-0.beta1.5
- Fix duplicate trigger indexes caused by beta1.3 fix (#1131960)

* Wed Aug 20 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-0.beta1.4
- Emergency hack for #1131892

* Mon Aug 18 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-0.beta1.3
- Fix regression on rpmspec dependency queries

* Mon Aug 18 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-0.beta1.2
- Fix regression on BuildRequires checking

* Mon Aug 18 2014 Panu Matilainen <pmatilai@redhat.com> - 4.12.0-0.beta1.1
- Update to 4.12.0-beta1 (http://rpm.org/wiki/Releases/4.12.0)
- Fixes #1122004, #1111349, #1117912, #1123722
- Drop upstreamed patches

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11.90-0.git12844.5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.90-0.git12844.5
- Fix wildcard database iterator (#1115824)

* Wed Jul 02 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.90-0.git12844.4
- Use autosetup for building rpm itself
- Hopefully fix armv7 vfp/neon detection

* Tue Jul 01 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.90-0.git12844.3
- Drop no longer needed temporary UsrMove patch
- Macro-expand load macro argument

* Mon Jun 30 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.90-0.git12844.2
- Fix multiple interleaved hardlink groups during build

* Mon Jun 30 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.90-0.git12844.1
- Update to rpm 4.12-alpha ((http://rpm.org/wiki/Releases/4.12.0)
- Drop/adjust patches as appropriate
- New sub-package(s) for plugins

* Thu Jun 26 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-17
- Clean up old, no longer needed cruft from spec

* Thu Jun 26 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-16
- Mark licenses as such, not documentation

* Wed Jun 25 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-15
- Perl dependency generators live in perl-generators (#1110823) now

* Wed Jun 18 2014 Lubomir Rintel <lkundrak@v3.sk> - 4.11.2-14
- Fix the armhfp patch for armv6hl

* Tue Jun 10 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-13
- Rawhide broke our test-suite, disable for now to allow builds to be done

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11.2-12.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 4.11.2-12
- Drop ChangeLog.bz2 (it's in the source, and it's large)

* Thu May 15 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 4.11.2-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Apr 21 2014 Tom Callaway <spot@fedoraproject.org> - 4.11.2-10
- remove _isa from all BuildRequires (bz 554854)
  See: https://fedoraproject.org/wiki/Packaging:Guidelines#BuildRequires_and_.25.7B_isa.7D

* Tue Apr 15 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-9
- move kmod and libsymlink dependency generators to redhat-rpm-config

* Mon Apr 14 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-8
- fix appdata.prov script missing from package

* Fri Apr 11 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-7
- disable sanitizers for now, needs more work...

* Fri Apr 11 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-6
- build with -fsanitize=address and -fsanitize=undefined for now
- add spec build conditional for sanitizer build

* Tue Apr 08 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-5
- replace unmaintained dependency generator scripts with rpmdeps wrappers

* Thu Mar 27 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-4
- revert #1045723 fix for now, it breaks some java package macros

* Wed Mar 26 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-3
- dont eat newlines on parametrized macro invocations (#1045723)
- fully reset file actions between rpmtsRun() calls (#1076552)
- fix build and sign module initialization in python3 (#1064758)

* Tue Feb 18 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-2
- reduce the double separator spec parse error into a warning (#1065563)

* Thu Feb 13 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-1
- update to 4.11.2 final (http://rpm.org/wiki/Releases/4.11.2)

* Thu Feb 06 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-0.rc2.1
- update to 4.11.2-rc2 (http://rpm.org/wiki/Releases/4.11.2)

* Mon Jan 20 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.2-0.rc1.1
- update to 4.11.2-rc1 (http://rpm.org/wiki/Releases/4.11.2)
- drop upstreamed patches, adjust others as needed
- handle python egg-info's version munging in file lists

* Wed Jan 15 2014 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-12
- include ppc64le in %%power64 macro (#1052930)

* Tue Dec 03 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-11
- generate kmod(module.ko) provides for kernel (#1025513)
- dont override CONFIG_SITE if already set (related to #962837)

* Mon Nov 18 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-10
- python 3 string and file compatibility fixes

* Mon Oct 14 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-9
- generate application() provides for gnome-software

* Tue Oct 01 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-8
- add support for ppc64le architecture

* Mon Sep 09 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-7
- fix build-time double-free on file capability processing (#956190)
- fix relocation related regression on file sanity check (#1001553)
- fix segfault on empty -p <lua> scriptlet body (#1004062)
- fix source url, once again

* Wed Aug 21 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-6
- add python3 sub-package, based on patch by Bohuslav Kabrda

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 4.11.1-5.1
- Perl 5.18 rebuild

* Fri Aug 02 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-5
- add missing dependency on tar to rpm-build (#986539)

* Tue Jul 30 2013 Florian Festi <ffesti@redhat.com> - 4.11.1-4
- Do not filter out lib64.* dependencies (#988373)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.11.1-3.1
- Perl 5.18 rebuild

* Fri Jul 05 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-3
- ensure relocatable packages always get install-prefix(es) set (#979443)

* Thu Jul 04 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-2
- fix .gnu_debuglink CRC32 after dwz, buildrequire binutils-devel (#971119)

* Thu Jun 27 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-1
- update to 4.11.1 final (http://rpm.org/wiki/Releases/4.11.1)

* Thu Jun 20 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-0.rc2.1
- update to 4.11.2-rc2 (http://rpm.org/wiki/Releases/4.11.1)
- drop upstreamed patches

* Mon Jun 17 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-0.rc1.4
- handle aarch64 debug_info relocations in debugedit (#974860)

* Tue Jun 11 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-0.rc1.3
- disable autoconf config.site processing in builds (#962837)

* Tue Jun 11 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-0.rc1.2
- fix regression on addressing main package by its name (#972994)

* Mon Jun 10 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.1-0.rc1.1
- update to 4.11.1-rc1 (http://rpm.org/wiki/Releases/4.11.1)

* Tue May 28 2013 Panu Matilainen <pmatilai@redhat.com> - - 4.11.0.1-7
- serialize BDB environment open/close (#924417)

* Wed May 22 2013 Panu Matilainen <pmatilai@redhat.com> - - 4.11.0.1-6
- only consider files with .pm suffix as perl modules (#927211)

* Fri May 17 2013 Panu Matilainen <pmatilai@redhat.com> - - 4.11.0.1-5
- filter out non-library soname dependencies

* Thu May 16 2013 Panu Matilainen <pmatilai@redhat.com> - - 4.11.0.1-4
- check for stale locks when opening write-cursors (#860500, #962750...)

* Fri May 10 2013 Tom Callaway <spot@fedoraproject.org> - 4.11.0.1-3
- lua 5.2 fix from upstream

* Mon Mar 25 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.0.1-2
- make rpm-build depend on virtual system-rpm-config provide

* Mon Feb 04 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.0.1-1
- update to 4.11.0.1 (http://rpm.org/wiki/Releases/4.11.0.1)

* Tue Jan 29 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.0-0.beta1.3
- revert yesterdays ghost-fix, it eats rpmdb's on upgrades

* Mon Jan 28 2013 Panu Matilainen <pmatilai@redhat.com> - 4.11.0-0.beta1.2
- armv7hl and armv7hnl should not have -mthumb (#901901)
- fix duplicate directory ownership between rpm and rpm-build (#894201)
- fix regression on paths shared between a real file/dir and a ghost

* Mon Dec 10 2012 Panu Matilainen <pmatilai@redhat.com> - 4.11.0-0.beta1.1
- update to 4.11 beta

* Mon Nov 19 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.90-0.git11989.3
- package /usr/lib/rpm/macros.d directory (related to #846679)
- fixup a bunch of old incorrect dates in spec changelog

* Sat Nov 17 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.90-0.git11989.2
- fix double-free on %%caps in spec (#877512)

* Thu Nov 15 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.90-0.git11989.1
- update to 4.11 (http://rpm.org/wiki/Releases/4.11.0) post-alpha snapshot
- drop/adjust patches as necessary

* Thu Oct 11 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.1-3
- fix noarch __isa_* macro filter in installplatform (#865436)

* Wed Oct 10 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.1-2
- account for intentionally skipped files when verifying hardlinks (#864622)

* Wed Oct 03 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.1-1
- update to 4.10.1 ((http://rpm.org/wiki/Releases/4.10.1)

* Mon Jul 30 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-6
- move our tmpfiles config to more politically correct location (#840192)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-5
- force _host_vendor to redhat to better match toolchain etc (#485203)

* Thu Jun 28 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-4
- merge ppc64p7 related fixes that only went into f17 (#835978)

* Wed Jun 27 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-3
- add support for minidebuginfo generation (#834073)

* Mon Jun 25 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-2
- add dwarf compression support to debuginfo generation (#833311)

* Thu May 24 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-1
- update to 4.10.0 final

* Mon Apr 23 2012 Panu Matilainen <pmatilai@redhat.com> - 4.10.0-0.beta1.1
- update to 4.10.0-beta1

* Mon Apr 16 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11536.1
- newer git snapshot (#809402, #808750)
- adjust posttrans script wrt bdb string change (#803866, #805613)

* Thu Apr 05 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11519.1
- newer git snapshot to keep patch-count down
- fixes CVE-2012-0060, CVE-2012-0061 and CVE-2012-0815
- fix obsoletes in installing set getting matched on provides (#810077)

* Wed Apr 04 2012 Jindrich Novy <jnovy@redhat.com> - 4.9.90-0.git11505.12
- rebuild against new libdb

* Tue Apr 03 2012 Jindrich Novy <jnovy@redhat.com> - 4.9.90-0.git11505.11
- build with internal libdb to allow libdb build with higher soname

* Fri Mar 30 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.10
- fix base arch macro generation (#808250)

* Thu Mar 29 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.9
- accept files as command line arguments to rpmdeps again (#807767)

* Mon Mar 26 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.8
- remove fake library provide hacks now that deltarpm got rebuilt

* Fri Mar 23 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.7
- fix header data length calculation breakage

* Thu Mar 22 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.6
- fix keyid size bogosity causing breakage on 32bit systems

* Wed Mar 21 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.5
- add temporary fake library provides to get around deltarpm "bootstrap"
  dependency (yes its dirty)

* Wed Mar 21 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.4
- fix overzealous sanity check breaking posttrans scripts

* Tue Mar 20 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.3
- fix bad interaction with yum's test-transaction and pretrans scripts

* Tue Mar 20 2012 Jindrich Novy <jnovy@redhat.com> - 4.9.90-0.git11505.2
- rebuild

* Tue Mar 20 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.90-0.git11505.1
- update to 4.10.0 alpha (http://rpm.org/wiki/Releases/4.10.0)
- drop/adjust patches as necessary

* Wed Mar 07 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-14
- fix backport thinko in the exclude patch

* Wed Mar 07 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-13
- fix memory corruption on rpmdb size estimation (#766260)
- fix couple of memleaks in python bindings (#782147)
- fix regression in verify output formatting (#797964)
- dont process spec include in false branch of if (#782970)
- only warn on missing excluded files on build (#745629)
- dont free up file info sets on test transactions

* Thu Feb 09 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-12
- switch back to smaller BDB cache default (#752897)

* Sun Jan 15 2012 Dennis Gilmore <dennis@ausil.us> - 4.9.1.2-11
- always apply arm hfp macros, conditionally apply the logic to detect hfp

* Tue Jan 10 2012 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-10
- adjust perl and python detection rules for libmagic change (#772699)

* Mon Jan 09 2012 Jindrich Novy <jnovy@redhat.com> - 4.9.1.2-9
- recognize perl script as perl code (#772632)

* Tue Dec 20 2011 Kay Sievers <kay@redhat.com> - 4.9.1.2-8
- add temporary rpmlib patch to support filesystem transition
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Dec 02 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-7
- switch over to libdb, aka Berkeley DB 5.x

* Thu Dec 01 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-6
- fix classification of ELF binaries with setuid/setgid bit (#758251)

* Fri Nov 25 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-5
- adjust font detection rules for libmagic change (#757105)

* Wed Nov 09 2011 Dennis Gilmore <dennis@ausil.us> - 4.9.1.2-4
- conditionally apply arm patch for hardfp on all arches but arm softfp ones

* Fri Oct 28 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-3
- adjust db util prefix & dependency due to #749293
- warn but dont fail the build if STABS encountered by debugedit (#725378)

* Wed Oct 12 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-2
- try teaching find-lang about the new gnome help layout (#736523)

* Thu Sep 29 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.2-1
- update to 4.9.1.2 (CVE-2011-3378)
- drop upstreamed rpmdb signal patch

* Mon Sep 19 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.1-3
- fix signal blocking/unblocking regression on rpmdb open/close (#739492)

* Mon Aug 08 2011 Adam Jackson <ajax@redhat.com> 4.9.1.1-2
- Add RPM_LD_FLAGS to build environment (#728974)

* Tue Aug 02 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1.1-1
- update to 4.9.1.1

* Tue Jul 19 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1-2
- fix recursion of directories with trailing slash in file list (#722474)

* Fri Jul 15 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.1-1
- update to 4.9.1 (http://rpm.org/wiki/Releases/4.9.1)
- drop no longer needed patches

* Thu Jun 16 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-10
- rebuild to fix a missing interpreter dependency due to bug #712251

* Fri Jun 10 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-9
- fix crash if prep or changelog section in spec is empty (#706959)
- fix crash on macro which undefines itself
- fix script dependency generation with file 5.07 string changes (#712251)

* Thu May 26 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-8
- add dwarf-4 support to debugedit (#707677)
- generate build-id symlinks for all filenames sharing a build-id (#641377)

* Thu Apr 07 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-7
- add missing ldconfig calls to build-libs sub-package
- fix source url

* Thu Apr 07 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-6
- revert the spec query change (#693338) for now, it breaks fedpkg

* Tue Apr 05 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-5
- verify some properties of replaced and wrong-colored files (#528383)
- only list packages that would be generated on spec query (#693338)
- preferred color packages should be erased last (#680261)
- fix leaks when freeing a populated transaction set
- take file state into account for file dependencies

* Tue Mar 22 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-4
- fix classification of elf executables with sticky bit set (#689182)

* Wed Mar 16 2011 Jindirch Novy <jnovy@redhat.com> - 4.9.0-3
- fix crash in package manifest check (#688091)

* Fri Mar 04 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-2
- fix duplicate rpmsign binary in rpm main package dragging in build-libs

* Wed Mar 02 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-1
- update to 4.9.0 final
- drop upstreamed patches

* Tue Mar 01 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.rc1.4
- spec cosmetics clean up extra whitespace + group more logically
- wipe out BDB environment at boot via tmpfiles.d

* Mon Feb 21 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.rc1.3
- fix erronous double cursor open, causing yum reinstall hang (#678644)

* Mon Feb 21 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.rc1.2
- fix broken logic in depgen collector, hopefully curing #675002

* Tue Feb 15 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.rc1.1
- update to 4.9.0-rc1
- drop upstream patches
- nss packaging has changed, buildrequire nss-softokn-freebl-devel

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.0-0.beta1.7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.7
- fix segfault when building more than one package at a time (#675565)

* Sun Feb 06 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.6
- adjust ocaml rule for libmagic string change

* Mon Jan 31 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.5
- dont try to remove environment files if private env used (related to #671200)
- unbreak mono dependency extraction (#673663)
- complain instead of silent abort if cwd is not readable (#672576)

* Tue Jan 25 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.4
- add support for Requires(posttrans) dependencies

* Fri Jan 21 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.3
- avoid division by zero in rpmdb size calculation (#671056)
- fix secondary index iteration returing duplicate at end (#671149)
- fix rebuilddb creating duplicate indexes for first header

* Fri Jan 21 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.2
- permit queries from rpmdb on read-only media (#671200)

* Tue Jan 18 2011 Panu Matilainen <pmatilai@redhat.com> - 4.9.0-0.beta1.1
- rpm 4.9.0-beta1 (http://rpm.org/wiki/Releases/4.9.0)
  - drop no longer needed patches
  - adjust requires + buildrequires to match current needs
  - adjust rpmdb index ghosts to match the new release
  - split librpmbuild and librpmsign to a separate rpm-build-libs package
  - split rpmsign to its own package to allow signing without all the build goo
  - build-conditionalize plugins, disabled for now
  - gstreamer and printer dependency generation moving out
  - handle .so symlink dependencies with fileattrs
  - use gnupg2 for signing as that's what typically installed by default

* Tue Jan 18 2011 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-7
- bunch of spec tweaks, cleanups + corrections:
  - shorten rpm-build filelist a bit with glob use, reorder for saner grouping
  - missing isa in popt version dependency
  - only add rpmdb_foo symlinks for actually relevant db_* utils
  - drop no longer necessary file-devel dependency from rpm-devel
  - drop sqlite backend build-conditional
  - preliminaries for moving from db4 to libdb
- use gnupg2 for signing as that's more likely to be installed by default

* Mon Oct 25 2010 Jindrich Novy <jnovy@redhat.com> - 4.8.1-6
- rebuild with new xz-5.0.0

* Tue Aug 10 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-5
- create gdb index on debuginfo generation (#617166)
- rpm-build now requires /usr/bin/gdb-add-index for consistent index creation
- include COPYING in -apidocs for licensing guidelines compliance

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 02 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-3
- ugh, reversed condition braindamage in the font provide extractor "fix"

* Wed Jun 30 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-2
- fix a potential getOutputFrom() error from font provide extraction
- debug-friendlier message to aid finding other similar cases (#565223)

* Fri Jun 11 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.1-1
- update to 4.8.1 (http://rpm.org/wiki/Releases/4.8.1)
- drop no longer needed patches
- fix source url pointing to testing directory

* Thu Jun 03 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-19
- also strip POSIX file capabilities from hardlinks on upgrade/erase (#598775)

* Wed Jun 02 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-18
- remove s-bits on upgrade too (#598775)

* Thu May 27 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-17
- fix segfault in spec parser (#597835)

* Thu May 27 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-16
- adjust to new pkg-config behavior wrt private dependencies (#596433)
- rpm-build now requires pkgconfig >= 0.24

* Fri May 21 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-15
- handle non-existent dependency sets correctly in python (#593553)
- make find-lang look in all locale dirs (#584866)

* Fri Apr 23 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-14
- lose dangling symlink to extinct (and useless) berkeley_db_svc (#585174)

* Wed Mar 24 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-13
- fix python match iterator regression wrt boolean representation

* Wed Mar 17 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-12
- unbreak find-lang --with-man from yesterdays braindamage

* Tue Mar 16 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-11
- support single PPD providing driver for devices (#568351)
- merge the psdriver patch pile into one
- preserve empty lines in spec prep section (#573339)
- teach python bindings about RPMTRANS_FLAG_NOCONTEXTS (related to #573111)
- dont own localized man directories through find_lang (#569536)

* Mon Feb 15 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-10
- drop bogus dependency on lzma, xz is used to handle the lzma format too

* Fri Feb 05 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-9
- unbreak python(abi) requires generation (#562906)

* Fri Feb 05 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-8
- more fixes to postscript provides extractor (#562228)
- avoid accessing unrelated mount points in disk space checking (#547548)
- fix disk space checking with erasures present in transaction (#561160)

* Fri Feb 05 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-7
- couple of fixes to the postscript provides extractor (#538101)

* Thu Feb 04 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-6
- extract provides for postscript printer drivers (#538101)

* Wed Feb 03 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-5
- python byte-compilation fixes + improvements (#558997)

* Sat Jan 30 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-4
- support parallel python versions in python dependency extractor (#532118)

* Thu Jan 21 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-3
- fix segfault on failed url retrieval
- fix verification error code depending on verbosity level
- if anything in testsuite fails, dump out the log

* Fri Jan 08 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-2
- put disttag back, accidentally nuked in 4.8.0 final update

* Fri Jan 08 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-1
- update to 4.8.0 final (http://rpm.org/wiki/Releases/4.8.0)

* Thu Jan 07 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.6
- pull out macro scoping "fix" for now, it breaks font package macros

* Mon Jan 04 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.5
- always clear locally defined macros when they go out of scope

* Thu Dec 17 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.4
- permit unexpanded macros when parsing spec (#547997)

* Wed Dec 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.3
- fix a bunch of python refcount-errors causing major memory leaks

* Mon Dec 07 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.2
- fix noise from python bytecompile on non-python packages (#539635)
- make all our -devel [build]requires isa-specific
- trim out superfluous -devel dependencies from rpm-devel

* Mon Dec 07 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.1
- update to 4.8.0-beta1 (http://rpm.org/wiki/Releases/4.8.0)
- rpm-build conflicts with current ocaml-runtime

* Fri Dec 04 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.2-2
- missing error exit code from signing password checking (#496754)
- dont fail build on unrecognized data files (#532489)
- dont try to parse subkeys and secret keys (#436812)
- fix chmod test on selinux, breaking %%{_fixperms} macro (#543035)

* Wed Nov 25 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.2-1
- update to 4.7.2 (http://rpm.org/wiki/Releases/4.7.2)
- fixes #464750, #529214

* Wed Nov 18 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-10
- rebuild against BDB-4.8.24

* Wed Nov 18 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-9
- drop versioned dependency to BDB

* Wed Oct 28 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-8
- support multiple python implementations in brp-python-bytecompile (#531117)
- make disk space problem reporting a bit saner (#517418)

* Tue Oct 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-7
- fix build with BDB 4.8.x by removing XA "support" from BDB backend
- perl dep extractor heredoc parsing improvements (#524929)

* Mon Sep 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-6
- use relative paths within db environment (related to #507309, #507309...)
- remove db environment on close in chrooted operation (related to above)
- initialize rpmlib earlier in rpm2cpio (#523260)
- fix file dependency tag extension formatting (#523282)

* Tue Sep 15 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-5
- fix duplicate dependency filtering on build (#490378)
- permit absolute paths in file lists again (#521760)
- use permissions 444 for all .debug files (#522194)
- add support for optional bugurl tag (#512774)

* Fri Aug 14 2009 Jesse Keating <jkeating@redhat.com> - 4.7.1-4
- Patch to make geode appear as i686 (#517475)

* Thu Aug 06 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-3
- rebuild because of the new xz

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-1
- update to 4.7.1 ((http://rpm.org/wiki/Releases/4.7.1)
- fix source url

* Mon Jul 20 2009 Bill Nottingham <notting@redhat.com> - 4.7.0-9
- enable XZ support

* Thu Jun 18 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-8
- updated OSGi dependency extractor (#506471)
- fix segfault in symlink fingerprinting (#505777)
- fix invalid memory access causing bogus file dependency errors (#506323)

* Tue Jun 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-7
- add dwarf-3 support to debugedit (#505774)

* Fri Jun 12 2009 Stepan Kasal <skasal@redhat.com> - 4.7.0-6
- require libcap >= 2.16 (#505596)

* Wed Jun 03 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-5
- don't mess up problem altNEVR in python ts.check() (#501068)
- fix hardlink size calculation on build (#503020)

* Thu May 14 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-4
- split cron-job into a sub-package to avoid silly deps on core rpm (#500722)
- rpm requires coreutils but not in %%post
- build with libcap and libacl
- fix pgp pubkey signature tag parsing

* Tue Apr 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-3
- couple of merge-review fixes (#226377)
  - eliminate bogus leftover rpm:rpm rpmdb ownership
  - unescaped macro in changelog
- fix find-lang --with-kde with KDE3 (#466009)
- switch back to default file digest algorithm

* Fri Apr 17 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-2
- file classification tweaks for text files (#494817)
  - disable libmagic text token checks, it's way too error-prone
  - consistently classify all text as such and include description

* Thu Apr 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-1
- update to 4.7.0 final (http://rpm.org/wiki/Releases/4.7.0)
- fixes #494049, #495429
- dont permit test-suite failure anymore

* Thu Apr 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.rc1.1
- update to 4.7.0-rc1
- fixes #493157, #493777, #493696, #491388, #487597, #493162

* Fri Apr 03 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.9
- fix recorded file state of otherwise skipped files (#492947)
- compress ChangeLog, drop old CHANGES file (#492440)

* Thu Apr  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4.7.0-0.beta1.8
- Fix sparcv9v and sparc64v targets

* Tue Mar 24 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.7
- prefer more specific types over generic "text" in classification (#491349)

* Mon Mar 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.6
- with the fd leak gone, let libmagic look into compressed files again (#491596)

* Mon Mar 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.5
- fix font provide generation on filenames with whitespace (#491597)

* Thu Mar 12 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.4
- handle RSA V4 signatures (#436812)
- add alpha arch ISA-bits
- enable internal testsuite on build

* Mon Mar 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.3
- fix _install_langs behavior (#489235)
- fix recording of file states into rpmdb on install

* Sun Mar 08 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.2
- load macros before creating directories on src.rpm install (#489104)

* Fri Mar 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.1
- update to 4.7.0-beta1 (http://rpm.org/wiki/Releases/4.7.0)

* Fri Feb 27 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-11
- build rpm itself with md5 file digests for now to ensure upgradability

* Thu Feb 26 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-10
- handle NULL passed as EVR in rpmdsSingle() again (#485616)

* Wed Feb 25 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-9
- pull out python byte-compile syntax check for now

* Mon Feb 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-8
- make -apidocs sub-package noarch
- fix source URL

* Sat Feb 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-7
- loosen up restrictions on dependency names (#455119)
- handle inter-dependent pkg-config files for requires too (#473814)
- error/warn on elf binaries in noarch package in build

* Fri Feb 20 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-6
- error out on uncompilable python code (Tim Waugh)

* Tue Feb 17 2009 Jindrich Novy <jnovy@redhat.com> - 4.6.0-5
- remove two offending hunks from anyarch patch causing that
  RPMTAG_BUILDARCHS isn't written to SRPMs

* Mon Feb 16 2009 Jindrich Novy <jnovy@redhat.com> - 4.6.0-4
- inherit group tag from the main package (#470714)
- ignore BuildArch tags for anyarch actions (#442105)
- don't check package BuildRequires when doing --rmsource (#452477)
- don't fail because of missing sources when only spec removal
  is requested (#472427)

* Mon Feb 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-3
- updated fontconfig provide script - fc-query does all the hard work now

* Mon Feb 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-2
- build against db 4.7.x

* Fri Feb 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-1
- update to 4.6.0 final
- revert libmagic looking into compressed files for now, breaks ooffice build

* Fri Feb 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.5
- enable fontconfig provides generation

* Thu Feb 05 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.4
- fixup rpm translation lookup to match Fedora specspo (#436941)

* Wed Feb 04 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.3
- extract mimehandler provides from .desktop files
- preliminaries for extracting font provides (not enabled yet)
- dont classify font metrics data as fonts
- only run script dep extraction once per file, duh

* Sat Jan 31 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.2
- change platform sharedstatedir to something more sensible (#185862)
- add rpmdb_foo links to db utils for documentation compatibility

* Fri Jan 30 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.1
- update to 4.6.0-rc4
- fixes #475582, #478907, #476737, #479869, #476201

* Fri Dec 12 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.2
- add back defaultdocdir patch which hadn't been applied on 4.6.x branch yet

* Fri Dec 12 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.1
- add dist-tag, rebuild

* Tue Dec 09 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.1
- update to rpm 4.6.0-rc3
- fixes #475214, #474550, #473239

* Wed Dec  3 2008 Jeremy Katz <katzj@redhat.com> - 4.6.0-0.rc2.9
- I built into the wrong place

* Wed Dec  3 2008 Jeremy Katz <katzj@redhat.com> - 4.6.0-0.rc2.8
- python 2.6 rebuild again

* Wed Dec 03 2008 Panu Matilainen <pmatilai@redhat.com>
- make rpm-build require pkgconfig (#473978)

* Tue Dec 02 2008 Panu Matilainen <pmatilai@redhat.com>
- fix pkg-config provide generation when pc's depend on each other (#473814)

* Mon Dec 01 2008 Jindrich Novy <jnovy@redhat.com>
- include rpmfileutil.h from rpmmacro.h, unbreaks
  net-snmp (#473420)

* Sun Nov 30 2008 Panu Matilainen <pmatilai@redhat.com>
- rebuild for python 2.6

* Sat Nov 29 2008 Panu Matilainen <pmatilai@redhat.com>
- update to 4.6.0-rc2
- fixes #471820, #473167, #469355, #468319, #472507, #247374, #426672, #444661
- enable automatic generation of pkg-config and libtool dependencies #465377

* Fri Oct 31 2008 Panu Matilainen <pmatilai@redhat.com>
- adjust find-debuginfo for "file" output change (#468129)

* Tue Oct 28 2008 Panu Matilainen <pmatilai@redhat.com>
- Florian's improved fingerprinting hash algorithm from upstream

* Sat Oct 25 2008 Panu Matilainen <pmatilai@redhat.com>
- Make noarch sub-packages actually work
- Fix defaultdocdir logic in installplatform to avoid hardwiring mandir

* Fri Oct 24 2008 Jindrich Novy <jnovy@redhat.com>
- update compat-db dependencies (#459710)

* Wed Oct 22 2008 Panu Matilainen <pmatilai@redhat.com>
- never add identical NEVRA to transaction more than once (#467822)

* Sun Oct 19 2008 Panu Matilainen <pmatilai@redhat.com>
- permit tab as macro argument separator (#467567)

* Thu Oct 16 2008 Panu Matilainen <pmatilai@redhat.com>
- update to 4.6.0-rc1
- fixes #465586, #466597, #465409, #216221, #466503, #466009, #463447...
- avoid using %%configure macro for now, it has unwanted side-effects on rpm

* Wed Oct 01 2008 Panu Matilainen <pmatilai@redhat.com>
- update to official 4.5.90 alpha tarball
- a big pile of misc bugfixes + translation updates
- isa-macro generation fix for ppc (#464754)
- avoid pulling in pile of perl dependencies for an unused script
- handle both "invalid argument" and clear env version mismatch on posttrans

* Thu Sep 25 2008 Jindrich Novy <jnovy@redhat.com>
- don't treat %%patch numberless if -P parameter is present (#463942)

* Thu Sep 11 2008 Panu Matilainen <pmatilai@redhat.com>
- add hack to support extracting gstreamer plugin provides (#438225)
- fix another macro argument handling regression (#461180)

* Thu Sep 11 2008 Jindrich Novy <jnovy@redhat.com>
- create directory structure for rpmbuild prior to build if it doesn't exist (#455387)
- create _topdir if it doesn't exist when installing SRPM
- don't generate broken cpio in case of hardlink pointing on softlink,
  thanks to pixel@mandriva.com

* Sat Sep 06 2008 Jindrich Novy <jnovy@redhat.com>
- fail hard if patch isn't found (#461347)

* Mon Sep 01 2008 Jindrich Novy <jnovy@redhat.com>
- fix parsing of boolean expressions in spec (#456103)
  (unbreaks pam, jpilot and maybe other builds)

* Tue Aug 26 2008 Jindrich Novy <jnovy@redhat.com>
- add support for noarch subpackages
- fix segfault in case of insufficient disk space detected (#460146)

* Wed Aug 13 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8461.2
- fix archivesize tag generation on ppc (#458817)

* Fri Aug 08 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8461.1
- new snapshot from upstream
- fixes #68290, #455972, #446202, #453364, #456708, #456103, #456321, #456913,
  #458260, #458261
- partial fix for #457360

* Thu Jul 31 2008 Florian Festi <ffesti@redhat.com>
- 4.5.90-0.git8427.1
- new snapshot from upstream

* Thu Jul 31 2008 Florian Festi <ffesti@redhat.com>
- 4.5.90-0.git8426.10
- rpm-4.5.90-posttrans.patch
- use header from rpmdb in posttrans to make anaconda happy

* Sat Jul 19 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.9
- fix regression in patch number handling (#455872)

* Tue Jul 15 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.8
- fix regression in macro argument handling (#455333)

* Mon Jul 14 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.7
- fix mono dependency extraction (adjust for libmagic string change)

* Sat Jul 12 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.6
- fix type mismatch causing funky breakage on ppc64

* Fri Jul 11 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.5
- flip back to external bdb
- fix tab vs spaces complaints from rpmlint
- add dep for lzma and require unzip instead of zip in build (#310694)
- add pkgconfig dependency to rpm-devel
- drop ISA-dependencies for initial introduction
- new snapshot from upstream for documentation fixes

* Thu Jul 10 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.4
- handle int vs external db in posttrans too

* Wed Jul 09 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.3
- require curl as external url helper

* Wed Jul 09 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.2
- add support for building with or without internal db

* Wed Jul 09 2008 Panu Matilainen <pmatilai@redhat.com>
- rpm 4.5.90-0.git8424.1 (alpha snapshot)
- adjust to build against Berkeley DB 4.5.20 from compat-db for now
- add posttrans to clean up db environment mismatch after upgrade
- forward-port devel autodeps patch

* Tue Jul 08 2008 Panu Matilainen <pmatilai@redhat.com>
- adjust for rpmdb index name change
- drop unnecessary vendor-macro patch for real
- add ISA-dependencies among rpm subpackages
- make lzma and sqlite deps conditional and disabled by default for now

* Fri Feb 01 2008 Panu Matilainen <pmatilai@redhat.com>
- spec largely rewritten, truncating changelog
