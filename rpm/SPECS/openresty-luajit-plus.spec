Name:           openresty-luajit-plus
Version:        20241015
Release:        1%{?dist}
Summary:        Luajit with enchance from openresty
Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com/

Source0:        luajit2-plus-%{version}.tar.gz

AutoReqProv:    no

%define plus_name    luajit2-plus
%define _missing_doc_files_terminate_build 0

%define prefix /usr/local/openresty/luajit-plus


BuildRoot: %{_tmppath}/%{plus_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc

%description
Luajit2 with enchance from OpenResty Inc.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{plus_name}-%{version}"; \
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


# ------------------------------------------------------------------------

%package devel
Summary:            Development files for %{name}
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Development files for Luajit


%prep
%setup -q -n %{plus_name}-%{version}


%build
make -j`nproc` CCDEBUG=-g XCFLAGS='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -g -DLUAJIT_ENABLE_GC64' Q= PREFIX=%{prefix}

%install
make install DESTDIR=%{buildroot} PREFIX=%{prefix}
rm -rf %{buildroot}%{prefix}/share/man
rm -rf %{buildroot}%{prefix}/lib/libluajit-5.1.a

pushd %{buildroot}

for f in `find .%{prefix}/ -type f -name '*.lua'`; do
    LUA_PATH=".%{prefix}/share/luajit-2.1/?.ljbc;.%{prefix}/share/luajit-2.1/?.lua;;" .%{prefix}/bin/luajit -bg $f ${f%.lua}.ljbc
    rm -f $f
done

popd

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%dir %{prefix}
%dir %{prefix}/bin
%dir %{prefix}/lib/lua/5.1
%dir %{prefix}/share/lua/5.1
%dir %{prefix}/share/lua
%dir %{prefix}/share/luajit-2.1
%dir %{prefix}/share/luajit-2.1/jit
%defattr(-,root,root,-)
%{prefix}/bin/luajit
%{prefix}/bin/luajit-2.1.*
%{prefix}/lib/libluajit-5.1.so
%{prefix}/lib/libluajit-5.1.so.2
%{prefix}/lib/libluajit-5.1.so.2.1.*
%{prefix}/share/luajit-2.1/jit/*.ljbc


%files devel
%defattr(-,root,root)
%dir %{prefix}/include/luajit-2.1
%dir %{prefix}/lib
%dir %{prefix}/lib/pkgconfig
%{prefix}/include/luajit-2.1/*.h
%{prefix}/include/luajit-2.1/*.hpp
%{prefix}/lib/pkgconfig/luajit.pc

%changelog
* Sat Nov 9 2024 Yichun Zhang (agentzh) 20241015-1
- upgraded luajit-plus to 20241015.
* Thu Aug 15 2024 Yichun Zhang (agentzh) 20240815-1
- upgraded luajit-plus to 20240815.
* Thu Jul 11 2024 Yichun Zhang (agentzh) 20240710-1
- upgraded luajit-plus to 20240710.
* Fri Jun 28 2024 Yichun Zhang (agentzh) 20240628-1
- upgraded luajit-plus to 20240628.
* Fri Jun 28 2024 Yichun Zhang (agentzh) 20240626-1
- upgraded luajit-plus to 20240626.
* Sun Jun 2 2024 Yichun Zhang (agentzh) 20240602-1
- upgraded luajit-plus to 20240602.
* Mon Mar 4 2024 Yichun Zhang (agentzh) 20240229-1
- upgraded luajit-plus to 20240229.
* Wed Nov 29 2023 Yichun Zhang (agentzh) 20231123-1
- upgraded luajit-plus to 20231123.
* Fri Oct 6 2023 Yichun Zhang (agentzh) 20231006-1
- upgraded luajit-plus to 20231006.
* Thu Oct 5 2023 Yichun Zhang (agentzh) 20230907-1
- upgraded luajit-plus to 20230907.
* Mon Apr 17 2023 Yichun Zhang (agentzh) 20230410-1
- upgraded luajit-plus to 20230410.
* Wed Jan 11 2023 Yichun Zhang (agentzh) 20230112-1
- upgraded luajit-plus to 20230112.
* Wed Jan 11 2023 Yichun Zhang (agentzh) 20230111-1
- upgraded luajit-plus to 20230111.
* Wed Jan 11 2023 Yichun Zhang (agentzh) 20230103-1
- upgraded luajit-plus to 20230103.
