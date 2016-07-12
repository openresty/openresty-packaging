Name
====

openresty-packaging - OpenResty packaging source and scripts for various Linux distributions.

Table of Contents
=================

* [Name](#name)
* [Fedora](#fedora)
* [CentOS/RHEL](#centosrhel)
* [Author](#author)
* [Copyright and License](#copyright-and-license)
* [See Also](#see-also)

Fedora
======

For Fedora 22+:

```bash
# create the makerpm account for building rpms only:
sudo useradd makerpm
sudo usermod -a -G mock makerpm
sudo passwd makerpm

# install rpm build tools:
sudo dnf install dnf install @development-tools fedora-packager rpmdevtools

# install openresty's build requirements:
sudo dnf install openssl-devel zlib-devel pcre-devel gcc make perl perl-Data-Dumper

# login as makerpm:
sudo su - makerpm

cd ~
rpmdev-setuptree

cd ~/rpmbuild/SOURCES/
cp /path/to/openresty-packaging/rpm/openresty.init ./
cp /path/to/openresty-packaging/rpm/*.patch ./

cd ~/rpmbuild/SPECS
cp /path/to/openresty-packaging/rpm/openresty.spec ./

rpmbuild -ba openresty.spec

```

If success, binary rpm files are under `~/rpmbuild/RPMS/` while source rpm files are under
`~/rpmbuld/SRPMS/`.

See the [How to create an RPM package wiki page](https://fedoraproject.org/wiki/How_to_create_an_RPM_package) for more details.

CentOS/RHEL
===========

For CentOS/RHEL 5+:

```bash
# create the makerpm account for building rpms only:
sudo useradd makerpm
sudo usermod -a -G mock makerpm
sudo passwd makerpm

# install rpm build tools:
sudo yum install rpm-build redhat-rpm-config

# install openresty's build requirements:
sudo dnf install openssl-devel zlib-devel pcre-devel gcc make perl perl-Data-Dumper

# login as makerpm:
sudo su - makerpm

mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

cd ~/rpmbuild/SOURCES/
cp /path/to/openresty-packaging/rpm/openresty.init ./
cp /path/to/openresty-packaging/rpm/*.patch ./

cd ~/rpmbuild/SPECS
cp /path/to/openresty-packaging/rpm/openresty.spec ./

rpmbuild -ba openresty.spec
```

See this [wiki page](https://wiki.centos.org/HowTos/SetupRpmBuildEnvironment) for more details.

Author
======

Yichun Zhang (agentzh) &lt;agentzh@gmail.com&gt;

[Back to TOC](#table-of-contents)

Copyright and License
=====================

This module is licensed under the BSD license.

Copyright (C) 2016 by Yichun "agentzh" Zhang (章亦春) &lt;agentzh@gmail.com&gt;, CloudFlare Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[Back to TOC](#table-of-contents)

See Also
========

* [OpenResty official site](https://openresty.org/)

[Back to TOC](#table-of-contents)

