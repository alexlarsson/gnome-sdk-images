#!/bin/sh

ROOT=`readlink -f $1`
VAR=`readlink -f $2`
IMAGE=`readlink -f $3`

rm -rf $ROOT
mkdir -p $ROOT
rm -rf $VAR
mkdir -p $VAR
(cd $ROOT; tar xvf $IMAGE > /dev/null; mv etc usr; mkdir -p $VAR/lib; mv var/lib/rpm $VAR/lib)
