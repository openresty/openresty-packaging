#!/bin/sh

for i in kernel-*debug.config; do
	base=`echo $i | sed -r s/-?debug//g`
	NEW=kernel-$VERSION-`echo $base | cut -d - -f2-`
	mv $i $NEW
	rm $base
done
