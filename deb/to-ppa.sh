#!/bin/bash

if [ -z "$1" ]; then
    echo No package name specified. > /dev/stderr
    exit 1
fi

for distro in artful xenial trusty zesty
do
    make $1-build OPTS=-S DISTRO=$distro
done
