Name:       openresty-postgresql
Version:    9.6.14
Release:    1%{?dist}
Summary:    PostgreSQL server

%define pgprefix %{_usr}/local/openresty/postgresql

Group:      Applications/System
License:    PostgreSQL License
URL:        http://www.postgresql.org/ftp/source/
Source0:	https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz
Source1:    openresty-postgresql.init

BuildRequires:  libxml2-devel libxslt-devel uuid-devel readline-devel openssl-devel
Requires:       libxml2 libxslt readline uuid openssl

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

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%prep
%setup -q -n postgresql-%{version}
./configure --prefix=%{pgprefix} \
            --with-libxml \
            --with-blocksize=32 \
            --with-segsize=2 \
            --with-wal-blocksize=64 \
            --with-libxslt \
            --with-openssl \
            --with-ossp-uuid \
            CFLAGS="-march=core2 -O2 -g3" \
            LDFLAGS="-Wl,-rpath,%{pgprefix}/lib"

%build
make %{?_smp_mflags}

%install
make install DESTDIR=${RPM_BUILD_ROOT}
make install-world DESTDIR=${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_ROOT}/%{pgprefix}/share/man \
    ${RPM_BUILD_ROOT}/%{pgprefix}/share/doc
#install -d $RPM_BUILD_ROOT/etc/ld.so.conf.d
install -d $RPM_BUILD_ROOT/etc/profile.d
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

%postun

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
%{pgprefix}/*
%exclude %{pgprefix}/include/*
%exclude %{pgprefix}/lib/*.a
/etc/init.d/openresty-postgresql


%files devel
%defattr(-,root,root,-)
%{pgprefix}/include/*
%{pgprefix}/lib/*.a
