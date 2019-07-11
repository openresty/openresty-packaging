#!/bin/bash

if [[ -z "$1" ]]; then
    echo No package name specified. > /dev/stderr
    exit 1
fi

if [[ "$1" == *"plus"* ]]; then
    echo "Cannot upload $1 to PPA" > /dev/stderr
    exit 1
fi

if [[ "$1" == *"edge"* ]]; then
    echo "Cannot upload $1 to PPA" > /dev/stderr
    exit 1
fi

if [[ "$1" == *"ip-database"* ]]; then
    echo "Cannot upload $1 to PPA" > /dev/stderr
    exit 1
fi

for distro in disco cosmic bionic xenial trusty
do
    make $1-build OPTS=-S DISTRO=$distro || exit 1
done
