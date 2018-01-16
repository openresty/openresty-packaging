Name:           lua-resty-ebpf-valgrind
Version:        0.1.0
Release:        1%{?dist}
Summary:        Lua module for manipulating Linux ebpf programs

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

Source0:        lua-resty-ebpf-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-c++ >= 4.8.5
BuildRequires:  make
BuildRequires:  openresty-bcc-devel >= 0.5.0-2
# LuaJIT is required to compile Lua files into byte code
BuildRequires:  openresty-plus

Requires:       openresty-bcc-devel >= 0.5.0-2
Requires:       openresty-iproute2 >= 4.13.0-1
Requires:       openresty-kernel >= 4.14.6-200
Requires:       openresty-kernel-devel >= 4.14.6-200
Requires:       openresty-plus-valgrind
Requires:       %{name}-data


%define orprefix                        %{_usr}/local/openresty-plus-valgrind
%define lua_lib_dir                     %{orprefix}/site/lualib
%define luajit                          %{_usr}/local/openresty-plus/luajit/bin/luajit

# Remove source code from debuginfo package.
# 1. generate the debuginfo meta
# 2. remove old source file directory, with all source files
# 3. create an empty source file directory to satify the requirement
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-resty-ebpf-%{version}/"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


%description
This package contains the Lua module for manipulating Linux ebpf programs.
It is almost the same as lua-resty-ebpf but for openresty-plus-valgrind package.

%package data

Summary:        The C data files for %{name} package
Group:          Development/Libraries
License:        GPLv2 and Redistributable
BuildArch:      noarch


%description data
This package contains the C data files for %{name} package.


%prep
# The $PWD is rpmbuild/BUILD
#../SPECS/get-lua-resty-ebpf %{version}
%setup -q -n "lua-resty-ebpf-%{version}"

%build
make CXXEXTRAFLAGS='-O0'
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
for f in `find lib/resty/ebpf -type f -name '*.lua'`; do
    %{luajit} -bg $f ${f%.lua}.ljbc
    rm $f
done

%install
rm -rf %{buildroot}
sed -i 's|lib/resty/ebpf/\*.lua|lib/resty/ebpf/\*.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}
make install_data DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%dir %{lua_lib_dir}/resty/ebpf
%{lua_lib_dir}/librestyebpf.so
%{lua_lib_dir}/resty/ebpf/*


%files data
%defattr(644,root,root,755)
%dir %{lua_lib_dir}/ebpf_data
%{lua_lib_dir}/ebpf_data/*


%changelog
* Mon Jan 15 2018 Zexuan Luo 0.1.0-1
- initial build for lua-resty-ebpf.
