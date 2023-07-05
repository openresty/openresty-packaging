%define prefix %{_usr}/local/openresty-tar

Name:           openresty-tar
Version:        1.32
Release:        6%{?dist}
Summary:        OpenResty's fork of tar.
Group:          Development/System
License:        GPLv3+
URL:            http://www.gnu.org/software/tar/

Source0:        https://ftp.gnu.org/gnu/tar/tar-%{version}.tar.gz

AutoReqProv: no

%define _rpmmacrodir %{_rpmconfigdir}/macros.d

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ccache, gcc >= 4.1.2-33
BuildRequires: autoconf, automake, gzip, texinfo
BuildRequires: gettext, libacl-devel, gawk

Requires: info
Requires: libacl
%if "%{?_vendor}" == "mariner"
Requires(post): /usr/bin/install-info
Requires(preun): /usr/bin/install-info
%else
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%endif

%description
OpenResty's fork of tar.

The GNU tar program saves many files together in one archive and can
restore individual files (or all of the files) from that archive. Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives, and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you also need to install
the rmt package on the remote box.

# ------------------------------------------------------------------------


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tar-%{version}"; \
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
%setup -q -n tar-%{version}


%build

CC='ccache gcc -fdiagnostics-color=always -fPIC' \
CFLAGS='-g3 -O2' \
    ./configure \
    --prefix=%{prefix}

make -j`nproc`

%install
make install DESTDIR=%{buildroot}

# remove useless files
rm -rf %{buildroot}%{prefix}/share/man
rm -rf %{buildroot}%{prefix}/share/locale
rm -rf %{buildroot}%{prefix}/share/info
rm -f %{buildroot}%{prefix}/libexec/rmt

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%dir %{prefix}
%dir %{prefix}/bin
%defattr(-,root,root)
%{prefix}/bin/*


# ------------------------------------------------------------------------

%changelog
* Sat Nov 02 2019 Jiahao Wang (johnny)
- initial packaging
