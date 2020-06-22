Name:           openresty-odb-debug
Version:        0.09
Release:        1%{?dist}
Summary:        The debug version of OpenResty Debugger based on ptrace
Group:          Development/System
License:        Proprietary
URL:            https://www.openresty.com/
Provides:       openresty-odb

Source0:        odb-%{version}.tar.gz

AutoReqProv:    no

#%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%define prefix /usr/local/openresty-odb-debug
%define pcre_prefix /opt/openresty-saas/pcre


%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ccache, gcc-c++
BuildRequires: openresty-saas-pcre-devel
Requires: openresty-saas-pcre

%description
OpenResty Debugger based on ptrace


# ------------------------------------------------------------------------

%package devel
Summary:            Development files for %{name} SaaS
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}


%description devel
Development files for OpenResty Debugger based on ptrace.


%prep
%setup -q -n odb-%{version}


%build
make %{?_smp_mflags} \
    CXX='ccache g++ -fdiagnostics-color=always' \
    PCRE=%{pcre_prefix} \
    CXXFLAGS="-DDDEBUG=1 -std=gnu++11 -g3 -Werror -Wall -O2 -I%{pcre_prefix}/include" \
    libodb-runtime.so

%install
make install DESTDIR=%{buildroot} PREFIX=%{prefix}

%clean
rm -rf %{buildroot}

# ------------------------------------------------------------------------

%files
%defattr(-,root,root,-)
%{prefix}/lib/libodb-runtime.so


%files devel
%defattr(-,root,root)
%{prefix}/include/odb-stat.h
%{prefix}/include/odb-runtime.h
%{prefix}/include/or-pcre.h
%{prefix}/include/or-utils.h


%changelog
* Sun Jun 21 2020 Yichun Zhang (agentzh) 0.09-1
- upgraded odb to 0.09.
* Sun Jun 21 2020 Yichun Zhang (agentzh) 0.08-1
- upgraded odb to 0.08.
* Fri Jun 19 2020 Jiahao Wang 0.07-1
- initial build for odb-debug 0.07-1.
