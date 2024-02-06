Name:               openresty-radare2-r2dec
Version:            0.0.2
Release:            1%{?dist}
Summary:            Converts asm to pseudo-C code for OpenResty

Group:              System Environment/Libraries

License:            LGPLv3
URL:                http://radare.org/
Source0:            r2dec-js-plus-%{version}.tar.gz

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      wget, openresty-python3, openresty-radare2-devel >= 5.0.3.3

Requires:           openresty-radare2 >= 5.0.3.3

AutoReqProv:        no

%define python3_prefix          /usr/local/openresty-python3
%define radare2_prefix          /usr/local/openresty-radare2

%description
Converts asm to pseudo-C code for OpenResty ONLY

%if 0%{?suse_version}

%debug_package

%else

# Remove source code from debuginfo package.
%define __debug_install_post \
    %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
    rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/r2dec-js-plus-%{version}"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
    mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/shlr"; \
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
%setup -q -n r2dec-js-plus-%{version}


%build
export PATH=$HOME/.local/bin:%{radare2_prefix}/bin:%{python3_prefix}/bin:$PATH
if [ -z "$(command -v $HOME/.local/bin/pip3)" ]; then
    wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
fi

if [ -z "$(command -v $HOME/.local/bin/meson)" ]; then
    pip3 install --user meson
fi

if [ -z "$(command -v $HOME/.local/bin/ninja)" ]; then
    pip3 install --user ninja
fi

make -C p -j`nproc`


%install
export PATH=$HOME/.local/bin:%{radare2_prefix}/bin:%{python3_prefix}/bin:$PATH
make install-plugin -C p DESTDIR=%{buildroot}


# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{radare2_prefix}/lib/radare2/*-git/libcore_pdd.so


%changelog
* Mon Feb 5 2024 Yichun Zhang (agentzh) 0.0.2-1
- upgraded openresty-radare2-r2dec to 0.0.2.
* Sun Feb 4 2024 Hui Wang 0.0.1-1
- initial build for openresty-radare2-r2dec.
