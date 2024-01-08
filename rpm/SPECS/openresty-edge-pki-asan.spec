Name:           openresty-edge-pki-asan
Version:        1.1.8
Release:        1%{?dist}
Summary:        OpenResty Edge Certificates Library

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

Source0:        edge-pki-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openresty-plus-core
BuildRequires:  openresty-plus-openssl111-asan-devel
Requires:       openresty-plus-core-asan

AutoReqProv:        no

%define or_prefix                       %{_usr}/local/openresty-plus
%define or_asan_prefix                  %{_usr}/local/openresty-plus-asan
%define lua_lib_dir                     %{or_prefix}/lualib
%define openssl_prefix                  %{or_asan_prefix}/openssl111


%description
Lua API for generating/verifying edge certificates.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/edge-pki-%{version}"; \
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
# The $PWD is rpmbuild/BUILD
%setup -q -n "edge-pki-%{version}"


%build
export CFLAGS="-g -I%{openssl_prefix}/include -fsanitize=address -fno-omit-frame-pointer"

make
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
for f in `find lib/oredge/ -type f -name '*.lua'`; do
    %{or_prefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm $f
done

%install
rm -rf %{buildroot}
sed -i 's|lib/oredge/\*.lua|lib/oredge/\*.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{or_asan_prefix}/lualib

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]

%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%dir %{or_asan_prefix}/lualib/oredge
%{or_asan_prefix}/lualib/libedgepki.so
%{or_asan_prefix}/lualib/oredge/*


%changelog
* Mon Jan 8 2024 Yichun Zhang (agentzh) 1.1.8-1
- upgraded openresty-edge-pki to 1.1.8.
* Mon Apr 17 2023 Yichun Zhang (agentzh) 1.1.7-1
- upgraded openresty-edge-pki to 1.1.7.
* Mon Dec 13 2021 Jiahao Wang (jiahao) 1.1.6-1
- upgraded openresty-edge-pki to 1.1.6.
* Wed Dec 1 2021 Yichun Zhang (agentzh) 1.1.5-1
- upgraded openresty-edge-pki to 1.1.5.
* Wed Nov 17 2021 Wang Hui (wanghuizzz) 1.1.4-1
- initial packaging.
