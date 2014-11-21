#!/bin/sh

ROOT=`pwd`/root
VAR=`pwd`/var
IMAGE=`readlink -f $1`

rm -rf $ROOT
mkdir -p $ROOT
rm -rf $VAR
mkdir -p $VAR
(cd $ROOT; tar xvf $IMAGE > /dev/null; mv etc usr; mkdir -p $VAR/lib; mv var/lib/rpm $VAR/lib)
