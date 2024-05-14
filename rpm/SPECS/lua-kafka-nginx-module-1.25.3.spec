Name:           lua-kafka-nginx-module-1.25.3
Version:        0.0.2
Release:        1%{?dist}
Summary:        Coroutine implemented using ucontext API

Group:          Development/Libraries

License:        Proprietary
URL:            https://www.openresty.com/

%define or_version           1.25.3.1

Source0:        lua-kafka-nginx-module-%{version}.tar.gz
Source1:        https://openresty.org/download/openresty-%{or_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  openresty >= 1.17.8.2
BuildRequires:  ccache, gcc, make, perl
BuildRequires:  openresty-openssl111-devel >= 1.1.1n-1
BuildRequires:  openresty-zlib-devel >= 1.2.12-1
BuildRequires:  openresty-pcre-devel
BuildRequires:  openresty-librdkafka-devel
BuildRequires:  openresty-cyrus-sasl-devel
BuildRequires:  openresty-ljsb-devel
Requires:       openresty-librdkafka, openresty-cyrus-sasl, openresty-ljsb


AutoReqProv:        no

%define or_prefix          /usr/local/openresty
%define zlib_prefix         %{or_prefix}/zlib
%define pcre_prefix         %{or_prefix}/pcre
%define openssl_prefix      %{or_prefix}/openssl111
%define ljsb_prefix         %{or_prefix}/ljsb
%define librdkafka_prefix   %{or_prefix}/librdkafka
%define lua_lib_dir         %{or_prefix}/site/lualib
%define sasl_prefix         /usr/local/openresty-plus/cyrus-sasl


%description
Coroutine implemented using ucontext API.


%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/lua-kafka-nginx-module-%{version}"; \
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
%setup -q -n "lua-kafka-nginx-module-%{version}"
tar xzf %{SOURCE1}


%build
# Create new file in install stage will cause check-buildroots to abort.
# To avoid it, we move the compilation in build stage.
for f in `find lualib/resty/ -type f -name '*.lua'`; do
    %{or_prefix}/luajit/bin/luajit -bg $f ${f%.lua}.ljbc
    rm $f
done

cd openresty-*/
./configure \
    --prefix="%{or_prefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include -I%{librdkafka_prefix}/include -I%{sasl_prefix}/include -I%{ljsb_prefix}/include -O3" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -L%{librdkafka}/lib -L%{sasl_prefix}/lib -L%{ljsb_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib:%{librdkafka_prefix}/lib:%{sasl_prefix}/lib:%{ljsb_prefix}/lib" \
    --with-compat --with-threads \
    --add-dynamic-module=../ \
    -j`nproc`

make -C build/nginx-*/ modules -j`nproc`


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{or_prefix}/nginx/modules

sed -i 's|lualib/resty/kafka/\*.lua|lualib/resty/kafka/\*.ljbc|g' Makefile
make install DESTDIR=%{buildroot} LUA_LIB_DIR=%{lua_lib_dir}

cd openresty-*/
install -m755 build/nginx-*/objs/*.so %{buildroot}%{or_prefix}/nginx/modules

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{or_prefix}/nginx/modules/ngx_http_lua_kafka_module.so
%{or_prefix}/site/lualib/resty/kafka/fast.ljbc


%changelog
* Mon May 13 2024 Yichun Zhang (agentzh) 0.0.2-1
- upgraded lua-kafka-nginx-module to 0.0.2.
* Tue Mar 7 2024 Junlong Li 0.0.1-1
- initial build for lua-kafka-nginx-module.
