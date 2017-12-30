#!/bin/sh

for i in kernel-*.config; do
	NEW=kernel-$VERSION-`echo $i | cut -d - -f2-`
	mv $i $NEW
done
