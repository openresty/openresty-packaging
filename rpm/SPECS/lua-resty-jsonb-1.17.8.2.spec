Name:           lua-resty-jsonb-1.17.8.2
Version:        0.0.1
Release:        2%{?dist}
Summary:        Lua module for manipulating jsonb data

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

Source0:        lua-resty-jsonb-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openresty-yajl-devel >= 2.1.0.4-1
# LuaJIT is required to compile Lua files into byte code
BuildRequires:  openresty = 1.17.8.2

Requires:  openresty-yajl >= 2.1.0.4-1

AutoReqProv:        no

%define orprefix                        %{_usr}/local/openresty
%define lua_lib_dir                     %{orprefix}/site/lualib

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-resty-jsonb-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%description
This package contains the Lua module for manipulating jsonb data which is compatible with json.


%prep
# The $PWD is rpmbuild/BUILD
%setup -q -n "lua-resty-jsonb-%{version}"

%build
make
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
for f in `find lib/resty/ -type f -name '*.lua'`; do
    %{orprefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm $f
done

%install
rm -rf %{buildroot}
sed -i 's|lib/resty/\*.lua|lib/resty/\*.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%dir %{lua_lib_dir}/resty
%{lua_lib_dir}/librestyjsonb.so
%{lua_lib_dir}/resty/*


%changelog
* Tue Sep 22 2020 Junlong Li 0.0.1-1
- initial build for lua-resty-jsonb.
