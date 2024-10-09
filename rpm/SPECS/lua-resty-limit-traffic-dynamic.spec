Name:           lua-resty-limit-traffic-dynamic
Version:        1.0.18
Release:        1%{?dist}
Summary:        limit HTTP request base on the traffic dynamically.

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

Source0:        lua-resty-limit-traffic-dynamic-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openresty >= 1.19.9
BuildRequires:  ccache, gcc, make


AutoReqProv:        no

%define or_prefix          /usr/local/openresty
%define lua_lib_dir        %{or_prefix}/site/lualib


%description
Limit HTTP request base on the traffic dynamically.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-resty-limit-traffic-dynamic-%{version}"; \
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
%setup -q -n "lua-resty-limit-traffic-dynamic-%{version}"

%build
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
for f in `find lib/resty/ -type f -name '*.lua'`; do
    %{or_prefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm $f
done

make -j`nproc`


%install
rm -rf %{buildroot}

sed -i 's|lib/resty/limit/traffic/dynamic/\*.lua|lib/resty/limit/traffic/dynamic/\*.ljbc|g' Makefile
sed -i 's|lib/resty/limit/traffic/dynamic.lua|lib/resty/limit/traffic/dynamic.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{or_prefix}/site/lualib/resty/limit/traffic/dynamic.ljbc
%{or_prefix}/site/lualib/resty/limit/traffic/dynamic/*.ljbc
%{or_prefix}/site/lualib/*.so


%changelog
* Tue Oct 8 2024 Yichun Zhang (agentzh) 1.0.18-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.18.
* Tue Oct 8 2024 Yichun Zhang (agentzh) 1.0.17-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.17.
* Tue Oct 8 2024 Yichun Zhang (agentzh) 1.0.16-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.16.
* Mon Oct 7 2024 Yichun Zhang (agentzh) 1.0.15-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.15.
* Thu Oct 3 2024 Yichun Zhang (agentzh) 1.0.14-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.14.
* Mon Sep 30 2024 Yichun Zhang (agentzh) 1.0.13-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.13.
* Sat Sep 28 2024 Yichun Zhang (agentzh) 1.0.12-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.12.
* Fri Sep 27 2024 Yichun Zhang (agentzh) 1.0.10-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.10.
* Thu Sep 26 2024 Yichun Zhang (agentzh) 1.0.9-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.9.
* Wed Sep 25 2024 Yichun Zhang (agentzh) 1.0.8-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.8.
* Tue Sep 24 2024 Yichun Zhang (agentzh) 1.0.7-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.7.
* Sun Sep 22 2024 Yichun Zhang (agentzh) 1.0.6-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.6.
* Wed Sep 11 2024 Yichun Zhang (agentzh) 1.0.5-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.5.
* Wed Sep 11 2024 Yichun Zhang (agentzh) 1.0.4-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.4.
* Mon Sep 9 2024 Yichun Zhang (agentzh) 1.0.3-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.3.
* Mon Sep 2 2024 Yichun Zhang (agentzh) 1.0.2-1
- upgraded lua-resty-limit-traffic-dynamic to 1.0.2.
* Sat Aug 31 2024 Yichun Zhang (agentzh) 1.0.0-1
- init version of lua-resty-limit-traffic-dynamic.
