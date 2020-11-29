# How to add a new packaging script.

## Add spec script of RPM package.

1. Choose a similar script from this repository.
   a. If you are packing a library software, refer to rpm/SPECS/openresty-openssl111.spec
   b. If you are packing a executable software, refer to rpm/SPECS/openresty-elfutils.spec
2. Copy the script you choose.
3. Modify the field of the to spec file to meet your new software.
   1. Refer to the spec in https://git.centos.org/projects/rpms/%2A. You can copy license, description and so on.
4. Use `spectool -g -R your-new-software.spec ` to download the source code If it is open source.
   a. If it is a Proprietary software, copy the tarball to ~/rpmbuild/SOURCES/
5. Use `rpmbuild -bb your-new-software.spec ` to build the new software.
6. Install the new rpm package in ~rpmbuild/RPMS/ with `rpm -ivh xxx.rpm`.
7. Test the software.
8. Add the update script.  eg `openresty-plus-packaging/rpm/SPECS/update-maxmind` and ``openresty-plus-packaging/deb/update-maxmind``

### Import Notes

1. If your are adding a new library packaging script, you may need to add the corresponding debug version script If this new library is installed in the default search path of openresty-plus.  eg: openresty-maxminddb.spec.

2. Make sure AutoReqProv is set to no: eg . `AutoReqProv: no`

3. Make sure Release is start from 1: eg `Release:        1%{?dist}`

4. Make sure source code is removed from debuginfo package

5. Make sure the software is build with "-g3 -O2" option.
6. build this package on CentOS6~CentOS8.

## Add deb script of deb package

1. clone the spec2deb repo to the same level of openresty-plus-packing:  git clone git@github.com:orinc/spec2deb
2. run the conversion command: ../spec2deb/bin/spec2deb.pl rpm/SPECS/your-new-software.spec
3. add clean target in deb/Makefile: your-new-software-clean
4. Remove `-fdiagnostics-color=always`  in deb/your-new-software/debian/rules.
5. Build this package on Ubuntu14 ~Ubuntu20.

