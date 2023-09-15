Name:               openresty-radare2
Version:            5.0.1
Release:            1%{?dist}
Summary:            radare2 for OpenResty

Group:              System Environment/Libraries

License:            LGPLv3
URL:                http://radare.org/
Source0:            radare2-plus-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

AutoReqProv:        no

%define radare2_prefix          /usr/local/openresty-radare2
%define radare2_data_prefix     /usr/local/openresty-radare2/share/radare2

%description
radare2 for OpenResty ONLY

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/radare2-plus-%{version}"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/shlr"; \
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
%setup -q -n radare2-plus-%{version}


%build
mkdir -p /usr/local/openresty-radare2/lib
CC='ccache gcc'
LDFLAGS='-Wl,-rpath,/usr/local/openresty-radare2/lib'
CFLAGS='-g -O2'
./configure --prefix=%{radare2_prefix} --with-rpath
make -j`nproc`


%install
make install DESTDIR=%{buildroot}

rm -f  %{buildroot}/%{radare2_prefix}/lib/*.a
rm -rf %{buildroot}/%{radare2_prefix}/lib/pkgconfig
rm -rf %{buildroot}/%{radare2_prefix}/include
rm -rf %{buildroot}/%{radare2_prefix}/share/man
rm -rf %{buildroot}/%{radare2_prefix}/share/doc
rm -rf %{buildroot}/%{radare2_data_prefix}/%{version}-git/www


# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{radare2_prefix}/bin/r*
%{radare2_prefix}/lib/libr*
%dir %{radare2_prefix}/lib/radare2/*-git
%{radare2_prefix}/lib/radare2/last
%dir %{radare2_data_prefix}
%dir %{radare2_data_prefix}/*-git
%dir %{radare2_data_prefix}/*-git/cons
%dir %{radare2_data_prefix}/*-git/syscall
%dir %{radare2_data_prefix}/*-git/opcodes
%dir %{radare2_data_prefix}/*-git/magic
%dir %{radare2_data_prefix}/*-git/fcnsign
%dir %{radare2_data_prefix}/*-git/charsets
%dir %{radare2_data_prefix}/*-git/flag
%dir %{radare2_data_prefix}/*-git/hud
%{radare2_data_prefix}/*-git/cons/*
%{radare2_data_prefix}/*-git/hud/*
%{radare2_data_prefix}/*-git/syscall/*
%{radare2_data_prefix}/*-git/opcodes/*
%{radare2_data_prefix}/*-git/magic/*
%{radare2_data_prefix}/*-git/fcnsign/*
%{radare2_data_prefix}/*-git/charsets/*
%{radare2_data_prefix}/*-git/flag/*
%{radare2_data_prefix}/last
%dir %{radare2_data_prefix}/*-git/format
%{radare2_data_prefix}/*-git/format/*


%changelog
* Fri Aug 25 2023 Hui Wang 5.0.0-1
- initial build for openresty-radare2.
