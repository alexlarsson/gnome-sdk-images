#!/bin/sh

REPO=$1
TAR=$2
TAR_VAR=$3
METADATA=$4
NAME=$5
ARCH=$6
VERSION=$7

rm -rf commit
mkdir -p commit
rm -rf commit-locales
mkdir -p commit-locales
echo "extracting ${TAR}"
tar xf ${TAR} -C commit
cp ${METADATA} commit/metadata

echo "extracting locales"
for F in commit/files/share/locale/*; do
    BASENAME=`basename $F`
    LOCALE=`basename $F | sed s/[@_].*//`
    mkdir -p commit-locales/$LOCALE/files/share
    mkdir -p commit/files/share/runtime/locale/$LOCALE/share/$BASENAME
    mv $F commit-locales/$LOCALE/files/share
    ln -s ../runtime/locale/$LOCALE/share/$BASENAME $F
done
for F in commit/files/lib/locale/*; do
    BASENAME=`basename $F`
    LOCALE=`basename $F | sed s/[@_].*//`
    mkdir -p commit-locales/$LOCALE/files/lib
    mkdir -p commit/files/share/runtime/locale/$LOCALE/lib/$BASENAME
    mv $F commit-locales/$LOCALE/files/lib
    ln -s ../../share/runtime/locale/$LOCALE/lib/$BASENAME $F
done

echo "commiting runtime/${NAME}/${ARCH}/${VERSION}"
ostree commit --repo=${REPO} --branch=runtime/${NAME}/${ARCH}/${VERSION} --owner-uid=0 --owner-gid=0 --disable-fsync --no-xattrs -s "release" commit

for F in commit-locales/*; do
    LOCALE=`basename $F`
    echo "commiting runtime/${NAME}.Locale.$LOCALE/${ARCH}/${VERSION}"
    ostree commit --repo=${REPO} --branch=runtime/${NAME}.Locale.$LOCALE/${ARCH}/${VERSION} --owner-uid=0 --owner-gid=0 --disable-fsync --no-xattrs -s "release" $F
done

rm -rf commit
mkdir -p commit
echo "extracting ${TAR_VAR}"
tar xf ${TAR_VAR} -C commit
echo "commiting runtime/${NAME}.Var/${ARCH}/${VERSION}"
ostree commit --repo=${REPO} --branch=runtime/${NAME}.Var/${ARCH}/${VERSION} --owner-uid=0 --owner-gid=0 --disable-fsync --no-xattrs -s "release" commit

if [ ${REPO} == "release/repo" ]; then
    echo "commiting generating deltas"
    ostree static-delta generate --repo=${REPO} --min-fallback-size 1 --empty runtime/${NAME}/x86_64/3.16
    ostree static-delta generate --repo=${REPO} --min-fallback-size 1 --empty runtime/${NAME}.Var/x86_64/3.16
fi

echo "commiting summary"
ostree summary -u --repo=${REPO}

echo "syncing"
sync
