#!/bin/bash

if [ -z "$1" ]; then
    echo No package name specified. > /dev/stderr
    exit 1
fi

for distro in zesty artful yakkety xenial trusty; do
    make $1-build OPTS=-S DISTRO=$distro
done
