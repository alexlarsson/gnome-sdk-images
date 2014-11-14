#!/bin/sh

ROOT=`readlink -e $1`
shift
VAR=`readlink -e $1`
shift
APP=`readlink -e $1`
shift

HELPER=`which gnome-sdk-helper`

declare -x HOME=/self
declare -x ACLOCAL_PATH="/self/share/aclocal"
declare -x CPLUS_INCLUDE_PATH="/self/include"
declare -x C_INCLUDE_PATH="/self/include"
declare -x GI_TYPELIB_PATH="/self/lib/girepository-1.0"
declare -x LDFLAGS="-L/self/lib "
declare -x PKG_CONFIG_PATH="/self/lib/pkgconfig:/self/share/pkgconfig"
declare -x PATH="/usr/bin:/self/bin"
unset INSTALL

$HELPER -w -W -a $APP -v $VAR $ROOT/usr "$@"
