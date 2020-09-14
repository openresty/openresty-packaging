Name:       openresty-postgresql
Version:    9.6.19
Release:    1%{?dist}
Summary:    PostgreSQL server

%define pgprefix %{_usr}/local/openresty/postgresql

Group:      Productivity/Database
License:    PostgreSQL License
URL:        http://www.postgresql.org/ftp/source/
Source0:	https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz
Source1:    openresty-postgresql.init

BuildRequires:  ccache, libxml2-devel, libxslt-devel, uuid-devel, readline-devel, openssl-devel
Requires:       libxml2, libxslt, readline, uuid, openssl

AutoReqProv:        no

%description
PostgreSQL is the world's most advanced open source database.

%package devel

Summary:    Development files for openresty-postgresql
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description devel
Provides C header and static library for the openresty-postgresql package.


# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/postgresql-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%prep
%setup -q -n postgresql-%{version}

%build
export GCC_COLORS="error=01;31:warning=01;35:note=01;36:range1=32:range2=34:locus=01:\
quote=01:fixit-insert=32:fixit-delete=31:\
diff-filename=01:diff-hunk=32:diff-delete=31:diff-insert=32:\
type-diff=01;32"

./configure --prefix=%{pgprefix} \
            --with-libxml \
            --with-blocksize=32 \
            --with-segsize=2 \
            --with-wal-blocksize=64 \
            --with-libxslt \
            --with-openssl \
            --with-ossp-uuid \
            CC='ccache gcc' \
            CFLAGS="-O2 -g3" \
            LDFLAGS="-L. -Wl,-rpath,%{pgprefix}/lib"

make %{?_smp_mflags}

%install
make install DESTDIR=${RPM_BUILD_ROOT}
make install-world DESTDIR=${RPM_BUILD_ROOT}

rm -rf ${RPM_BUILD_ROOT}/%{pgprefix}/share/man \
    ${RPM_BUILD_ROOT}/%{pgprefix}/share/doc

rm -f ${RPM_BUILD_ROOT}/%{pgprefix}/lib/*/*.o \
    ${RPM_BUILD_ROOT}/%{pgprefix}/lib/st[a-zA-Z0-9]*

#install -d $RPM_BUILD_ROOT/etc/ld.so.conf.d
#install -d $RPM_BUILD_ROOT/etc/profile.d
install -d $RPM_BUILD_ROOT/etc/init.d
%{__install} -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/etc/init.d/openresty-postgresql

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%post
#/sbin/ldconfig
/sbin/chkconfig --add openresty-postgresql


%preun
if [ $1 = 0 ]; then
   /sbin/service openresty-postgresql stop >/dev/null 2>&1
   /sbin/chkconfig --del openresty-postgresql
fi

%clean
rm -fr $RPM_BUILD_ROOT

%pre
if [ $1 == 1 ];then
    id -u postgres > /dev/null
    rc=$?
    if [ $rc -ne 0 ]; then
        groupadd postgres || exit 1
        useradd -g postgres postgres || exit 1
    fi
    mkdir -p /var/postgres
    mkdir -p /var/postgres/{data,scripts,conf,log}
    chown -R postgres:postgres /var/postgres
fi


%files
%defattr(-, root, root)
%{pgprefix}/bin/*
%{pgprefix}/lib/*.so
%{pgprefix}/lib/*.so.*
%{pgprefix}/lib/pgxs/*
%{pgprefix}/share/*
/etc/init.d/openresty-postgresql


%files devel
%defattr(-,root,root,-)
%{pgprefix}/include/*
%{pgprefix}/lib/*.a
%{pgprefix}/lib/pkgconfig/*
