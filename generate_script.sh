#!/bin/sh
for i in $@; do
    PROG=`rpm -qp --qf '%{POSTINPROG}' $i`
    if [ $PROG == '(none)' -o $PROG == '/sbin/ldconfig'  ]; then
        true;
    elif [ $PROG == '/bin/sh' ]; then
        echo "#from `basename $i`";
        rpm -qp --qf '%{POSTIN}\n' $i
    else
        echo $PROG not supported
        exit 1
    fi
done
for i in $@; do
    PROG=`rpm -qp --qf '%{POSTTRANSPROG}' $i`
    if [ $PROG == '(none)' -o $PROG == '/sbin/ldconfig'  ]; then
        true;
    elif [ $PROG == '/bin/sh' ]; then
        echo "#from `basename $i`";
        rpm -qp --qf '%{POSTTRANS}\n' $i
    else
        echo $PROG not supported
        exit 1
    fi
done
echo "#always"
echo /sbin/ldconfig
