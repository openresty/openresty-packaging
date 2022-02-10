Name:           lua-resty-wasm
Version:        0.0.1
Release:        1%{?dist}
Summary:        The Wasm library for OpenResty

Group:          System Environment/Libraries

License:        Proprietary
URL:            https://github.com/orinc/lua-resty-wasm
Source0:        lua-resty-wasm-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openresty-elf-loader-devel
BuildRequires:  openresty-elfutils-devel
Requires:       openresty-elf-loader
Requires:       openresty-elfutils

AutoReqProv:        no

%define orprefix                        %{_usr}/local/openresty-plus
%define lua_lib_dir                     %{orprefix}/site/lualib
%define wasm_dir                        %{orprefix}/wasm


%description
The wasm library use by OpenResty ONLY


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-resty-wasm-%{version}"; \
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

Summary:            Development files for OpenResty's wasm library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty's wasm library.


%prep
%setup -q -n lua-resty-wasm-%{version}


%build
make -j`nproc` OPENRESTY_PREFIX=%{orprefix}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir} OPENRESTY_PREFIX=%{orprefix}


%clean
rm -rf %{buildroot}


# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%files devel
%defattr(-,root,root,-)
%{wasm_dir}/include/wasm-rt.h
%{wasm_dir}/include/or-wasm.h
%{wasm_dir}/include/or-arch.h

%files
%defattr(0755,root,root,-)
%{wasm_dir}/lib/liborwasmrt.so
%{lua_lib_dir}/resty/wasm-elf-loader.ljbc


%changelog
* Tue Feb 8 2022 Yichun Zhang 0.0.1
- initial version
