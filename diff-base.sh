#!/bin/sh
for i in freedesktop-sdk-images/specs/*.spec; do
    if test -f specs/`basename $i`; then
        diff -u $i specs/`basename $i`;
    fi;
done
