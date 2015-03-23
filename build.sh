#!/bin/sh

ROOT=`pwd`/build/root
VAR=`pwd`/build/var
APP=`pwd`/packages
SRC=`pwd`/

HELPER=`which linux-user-chroot`

declare -x LC_ALL=en_US.utf8
declare -x HOME=/self
unset ACLOCAL_FLAGS
declare -x ACLOCAL_PATH="/self/share/aclocal"
declare -x CPLUS_INCLUDE_PATH="/self/include"
declare -x C_INCLUDE_PATH="/self/include"
declare -x GI_TYPELIB_PATH="/self/lib/girepository-1.0"
declare -x LDFLAGS="-L/self/lib "
declare -x LD_LIBRARY_PATH="/self/lib"
declare -x PATH="/usr/bin:/self/bin"
declare -x PKG_CONFIG_PATH="/self/lib/pkgconfig:/self/share/pkgconfig"
declare -x XDG_CONFIG_DIRS="/self/etc/xdg:/etc/xdg"
declare -x XDG_DATA_DIRS="/self/share:/usr/share"
if test -d packages/.ccache; then
    declare -x PATH="/self/bin/ccache:$PATH"
fi
unset PYTHONPATH
unset INSTALL
unset PERL5LIB

CHROOT=`mktemp -d`
mkdir $CHROOT/var
mkdir $CHROOT/usr
mkdir $CHROOT/tmp
mkdir $CHROOT/self
mkdir $CHROOT/proc
mkdir $CHROOT/dev
mkdir $CHROOT/src
ln -s usr/lib $CHROOT/lib
ln -s usr/bin $CHROOT/bin
ln -s usr/sbin $CHROOT/sbin
ln -s usr/etc $CHROOT/etc

cp -a $ROOT/usr/etc/passwd $CHROOT
cp -a $ROOT/usr/etc/group $CHROOT
cp  /etc/passwd $ROOT/usr/etc/
cp  /etc/group $ROOT/usr/etc/

$HELPER --unshare-ipc --unshare-pid --unshare-net --mount-bind /dev /dev --mount-proc /proc --mount-bind $ROOT/usr /usr --mount-bind $VAR /var --mount-bind $APP /self  --mount-bind $SRC /src --chdir /src $CHROOT "$@"

cp -a $CHROOT/passwd $ROOT/usr/etc/
cp -a $CHROOT/group $ROOT/usr/etc/

rm -rf $CHROOT
