#!/bin/sh

REPO=$1
TAR=$2
TAR_VAR=$3
METADATA=$4
NAME=$5
ARCH=$6
VERSION=$7

set -x

rm -rf commit
mkdir -p commit
tar xf ${TAR} -C commit
cp ${METADATA} commit/metadata
ostree commit --repo=${REPO} --branch=runtime/${NAME}/${ARCH}/${VERSION} --owner-uid=0 --owner-gid=0 --disable-fsync --no-xattrs -s "release" commit

rm -rf commit
mkdir -p commit
tar xf ${TAR_VAR} -C commit
ostree commit --repo=${REPO} --branch=runtime/${NAME}.Var/${ARCH}/${VERSION} --owner-uid=0 --owner-gid=0 --disable-fsync --no-xattrs -s "release" commit

if [ ${REPO} == "release/repo" ]; then
    ostree static-delta generate --repo=${REPO} --min-fallback-size 1 --empty runtime/${NAME}/x86_64/3.16
    ostree static-delta generate --repo=${REPO} --min-fallback-size 1 --empty runtime/${NAME}.Var/x86_64/3.16
fi

ostree summary -u --repo=${REPO}
