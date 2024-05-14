Name:           replace-filter-plus-nginx-module-1.21.4
Version:        0.0.3
Release:        1%{?dist}
Summary:        Streaming regular expression replacement in response bodies

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

%define pkg_name       replace-filter-nginx-module-plus
%define ngx_version    1.21.4
%define or_version     %{ngx_version}.1

Source0:        %{pkg_name}-%{version}.tar.gz
Source1:        openresty-%{or_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define perl_ver_rel        5.24.4-8

BuildRequires:  ccache, gcc, make, perl
BuildRequires:  openresty-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-pcre-devel
BuildRequires:  openresty-perl >= %{perl_ver_rel}
BuildRequires:  openresty-perl-B-C >= 1.57-7
BuildRequires:  openresty-perl-devel >= %{perl_ver_rel}
BuildRequires:  openresty-perl-IPC-Run3


AutoReqProv:        no

%define prefix              /usr/local/openresty
%define zlib_prefix         %{prefix}/zlib
%define pcre_prefix         %{prefix}/pcre
%define openssl_prefix      %{prefix}/openssl111

%define perlcc              /usr/local/openresty-perl/bin/perlcc
%define tmp_luajit_prefix   /openresty-%{or_version}/build/luajit-root/%{prefix}/luajit

%description
Streaming regular expression replacement in response bodies.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/%{pkg_name}-%{version}"; \
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
Summary:            Development files for %{name}
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Development files for %{name}.

Requires:       openresty-perl >= %{perl_ver_rel}


%prep
%setup -q -n "%{pkg_name}-%{version}"
%setup -q -a 1 -n "%{pkg_name}-%{version}"


%build
%{perlcc} -v4 -O2 --Wc='-g -O2' -o "bin/split-sm" "bin/split-sm.pl" \
    && if [ ! -f "bin/split-sm" ]; then exit 1; fi

cd openresty-%{or_version}/
./configure \
    --prefix="%{prefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -O3" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
    --with-compat \
    --add-dynamic-module=../ \
    -j`nproc`

make -C build/nginx-%{ngx_version}/ modules -j`nproc`


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{prefix}/lib
mkdir -p %{buildroot}%{prefix}/site/lualib

# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
for f in `find lib/resty/ -type f -name '*.lua'`; do
    LUA_PATH="./%{tmp_luajit_prefix}/share/luajit-2.1/?.lua;./%{tmp_luajit_prefix}/share/luajit-2.1.0-beta3/?.lua;;" \
        ./%{tmp_luajit_prefix}/bin/luajit \
        -bg $f ${f%.lua}.ljbc
    rm $f
done

cp -r lib/resty %{buildroot}%{prefix}/site/lualib/
install -d %{buildroot}%{prefix}/bin
install -d %{buildroot}%{prefix}/nginx/modules
install -m755 openresty-%{or_version}/build/nginx-%{ngx_version}/objs/*.so \
    %{buildroot}%{prefix}/nginx/modules/
install -m755 bin/split-sm %{buildroot}%{prefix}/bin/split-sm

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{prefix}/nginx/modules/ngx_http_replace_filter_module.so
%{prefix}/site/lualib/resty/replace.ljbc


%files devel
%defattr(-,root,root)
%{prefix}/bin/split-sm


%changelog
* Mon May 13 2024 Yichun Zhang (agentzh) 0.0.3-1
- upgraded replace-filter-nginx-module to 0.0.3.
* Sat May 11 2024 Yichun Zhang (agentzh) 0.0.2-1
- upgraded replace-filter-nginx-module to 0.0.2.
* Thu May 09 2024 Jiahao Wang 0.0.1-1
- initial build for replace-filter-nginx-module.
