#!/bin/sh

ROOT=`readlink -f $1`
VAR=`readlink -f $2`
IMAGE=`readlink -f $3`

rm -rf $ROOT
mkdir -p $ROOT
rm -rf $VAR
mkdir -p $VAR
(cd $ROOT; tar xvf $IMAGE > /dev/null; mv etc usr)
./build.sh $ROOT $VAR $VAR smart channel -y --add mydb type=rpm-sys name="RPM Database"
./build.sh $ROOT $VAR $VAR smart channel -y --add noarch type=rpm-dir name="RPM Database" path=/self/RPMS/noarch
./build.sh $ROOT $VAR $VAR smart channel -y --add x86_64 type=rpm-dir name="RPM Database" path=/self/RPMS/x86_64/
