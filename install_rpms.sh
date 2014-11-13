#!/bin/sh

set -x
smart install --urls $@ 2> package.list
FILES=
for i in `cat package.list | grep -v "warning:" | sed "s#file:///#/#"`; do
    FILES="$FILES $i"
    rpm2cpio $i | (cd /self/gnome-platform; cpio -id)
done
./generate_script.sh $FILES > /self/gnome-platform/post_install.sh
mv /self/gnome-platform/etc/* /self/gnome-platform/usr/etc/
mv /self/gnome-platform/lib/* /self/gnome-platform/usr/lib/
mv /self/gnome-platform/bin/* /self/gnome-platform/usr/bin/
