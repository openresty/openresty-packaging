Name:       openresty-postgresql12
Version:    12.5
Release:    7%{?dist}
Summary:    PostgreSQL server

%define pgprefix            %{_usr}/local/openresty-postgresql12
%define openssl_prefix      %{_usr}/local/openresty-plus/openssl111

Group:      Productivity/Database
License:    PostgreSQL License
URL:        http://www.postgresql.org/ftp/source/
Source0:	https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz
Source1:    openresty-postgresql12.init
Source2:    openresty-postgresql12.service

BuildRequires:  ccache, libxml2-devel, libxslt-devel, uuid-devel, readline-devel, openresty-plus-openssl111-devel

Requires:   openresty-plus-openssl111

%if 0%{?suse_version}
Requires:   libxslt1

%if %{suse_version} <= 1315
Requires:   libreadline6
%else
Requires:   libreadline7
%endif

Requires:   libossp-uuid16
Requires:   libxml2-2
%else
Requires:   libxslt
Requires:   readline
Requires:   uuid
Requires:   libxml2
%endif

AutoReqProv:        no

%description
PostgreSQL is the world's most advanced open source database.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/postgresql-%{version}"; \
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


%package devel

Summary:    Development files for openresty-postgresql12
Group:      Applications/System
Requires:   %{name} = %{version}-%{release}

%description devel
Provides C header and static library for the openresty-postgresql12 package.


%prep
%setup -q -n postgresql-%{version}

%build
export GCC_COLORS="error=01;31:warning=01;35:note=01;36:range1=32:range2=34:locus=01:\
quote=01:fixit-insert=32:fixit-delete=31:\
diff-filename=01:diff-hunk=32:diff-delete=31:diff-insert=32:\
type-diff=01;32"

./configure --prefix="%{pgprefix}" \
            --libdir="%{pgprefix}/lib" \
            --with-libraries="%{openssl_prefix}/lib" \
            --with-libxml \
            --with-blocksize=32 \
            --with-segsize=2 \
            --with-wal-blocksize=64 \
            --with-libxslt \
            --with-openssl \
            --with-ossp-uuid \
            CC='ccache gcc' \
            CFLAGS="-O2 -g3 -I%{openssl_prefix}/include" \
            LDFLAGS="-L. -Wl,-rpath,%{pgprefix}/lib,-rpath,%{openssl_prefix}/lib"

make -j`nproc` MAKELEVEL=0


%install
make install DESTDIR=${RPM_BUILD_ROOT} MAKELEVEL=0

make install-world DESTDIR=${RPM_BUILD_ROOT} MAKELEVEL=0

rm -rf ${RPM_BUILD_ROOT}/%{pgprefix}/share/man \
    ${RPM_BUILD_ROOT}/%{pgprefix}/share/doc

rm -f ${RPM_BUILD_ROOT}/%{pgprefix}/lib/*/*.o \
    ${RPM_BUILD_ROOT}/%{pgprefix}/lib/st[a-zA-Z0-9]*

#install -d $RPM_BUILD_ROOT/etc/ld.so.conf.d
#install -d $RPM_BUILD_ROOT/etc/profile.d
install -d $RPM_BUILD_ROOT/etc/init.d
install -d $RPM_BUILD_ROOT/%{pgprefix}/share/systemd
%{__install} -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/etc/init.d/openresty-postgresql12
%{__install} -p -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/%{pgprefix}/share/systemd/openresty-postgresql12.service

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%post
#/sbin/ldconfig
if [ -d "/etc/systemd/system" ]; then
    cp -f %{pgprefix}/share/systemd/openresty-postgresql12.service \
       /etc/systemd/system/openresty-postgresql12.service
    /bin/systemctl daemon-reload
    /bin/systemctl stop openresty-postgresql12 >/dev/null 2>&1

else
    /sbin/chkconfig --add openresty-postgresql12
fi



%preun
if [ $1 = 0 ]; then
    if [ -d "/etc/systemd/system" ]; then
        /bin/systemctl stop openresty-postgresql12 >/dev/null 2>&1
        rm -f /etc/systemd/system/openresty-postgresql12.service

    elif [ -n "$(command -v service)" ]; then
        $(command -v service) openresty-postgresql12 stop >/dev/null 2>&1
    fi

    if [ -n "$(command -v chkconfig)" ]; then
        $(command -v chkconfig) --del openresty-postgresql12
    fi
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
    mkdir -p /var/postgres12
    mkdir -p /var/postgres12/{data,scripts,conf,log}
    chown -R postgres:postgres /var/postgres12
fi


%files
%defattr(-, root, root)
%{pgprefix}/bin/*
%{pgprefix}/lib/*.so
%{pgprefix}/lib/*.so.*
%{pgprefix}/lib/pgxs/*
%{pgprefix}/share/*
/etc/init.d/openresty-postgresql12


%files devel
%defattr(-,root,root,-)
%{pgprefix}/include/*
%{pgprefix}/lib/*.a
%{pgprefix}/lib/pkgconfig/*
