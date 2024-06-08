Name:               openresty-librdkafka
Version:            2.4.0
Release:            1%{?dist}
Summary:            Apache Kafka C driver library.

Group:              System Environment/Libraries

License:            Proprietary
URL:                https://github.com/confluentinc/librdkafka
Source0:            https://github.com/confluentinc/librdkafka/archive/refs/tags/v%{version}.tar.gz
Patch0:             librdkafka-const-int.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      libtool, openresty-openssl111-devel, openresty-cyrus-sasl-devel

Requires:           openresty-openssl111, openresty-cyrus-sasl

AutoReqProv:        no

%define kafka_prefix    /usr/local/openresty/librdkafka
%define sasl_prefix     /usr/local/openresty-plus/cyrus-sasl
%define ssl_prefix      /usr/local/openresty/openssl111

%description
librdkafka is a C library implementation of the Apache Kafka protocol, providing Producer, Consumer and Admin clients. It was designed with message delivery reliability and high performance in mind, current figures exceed 1 million msgs/second for the producer and 3 million msgs/second for the consumer.

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/librdkafka-%{version}"; \
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

Summary:            Development files for OpenResty's librdkafka library
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Provides C header and static library for OpenResty's librdkafka library.


%prep
%setup -q -c -n librdkafka-%{version}
mv librdkafka-%{version}/* .

%patch0 -p1

%build
CFLAGS="-I%{ssl_prefix}/include -I%{sasl_prefix}/include" \
LDFLAGS="-L%{ssl_prefix}/lib -L%{sasl_prefix}/lib -g -O2 -Wl,-rpath,%{ssl_prefix}/lib:%{sasl_prefix}/lib" \
./configure --disable-curl --disable-gssapi --disable-lz4-ext --enable-ssl --disable-zstd --enable-gssapi --prefix=%{kafka_prefix}
make -j$(nproc) libs


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{kafka_prefix}/share
rm -f  %{buildroot}/%{kafka_prefix}/lib/*.la

export QA_RPATHS=$(( 0x0020|0x0001|0x0010|0x0002 ))


%clean
rm -rf %{buildroot}


%files
%{kafka_prefix}/lib/*.so
%{kafka_prefix}/lib/*.so.*


%files devel
%{kafka_prefix}/include/librdkafka/*.h
%{kafka_prefix}/lib/pkgconfig/*.pc
%{kafka_prefix}/lib/librdkafka*.a


%changelog
* Tue May 7 2024 Yichun Zhang (agentzh) 2.4.0
- upgraded openresty-kafka to 2.4.0.
