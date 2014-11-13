SPECS="$@"
export LC_ALL=C
rm -rf /tmp/dep
mkdir -p /tmp/dep

# Generate mapping package name => package name + full version + arch
for spec in $SPECS; do
   export spec
   bash -c "`rpmspec -q $spec --qf 'echo packages/RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm > /tmp/dep/%{NAME}.pkg;'`";
done

ALL_SOURCES=

for spec in $SPECS; do
    SOURCES=`rpmspec -P $spec | grep "^Source.*:" | awk '{ print $2 }' /dev/stdin | grep 'http\|ftp'`
    for i in $SOURCES; do
        echo packages/SOURCES/`basename $i`:;
        echo -e "\twget -P packages/SOURCES/ $i\n";
        ALL_SOURCES="$ALL_SOURCES packages/SOURCES/`basename $i`";
    done

    PACKAGES=`rpmspec -q ${spec} --qf 'packages/RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm '`
    BUILDREQS=`rpmspec -q ${spec} --buildrequires`
    BRS=""
    for br in $BUILDREQS; do
        BRS="$BRS `cat /tmp/dep/${br}.pkg`"
    done
    echo "$PACKAGES: $spec $BRS setup.sh build.sh yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz"
    echo "	echo building $spec"
    echo "	./setup.sh root-sdk var-sdk yocto-build/x86_64/images/gnomeos-contents-sdk-x86_64.tar.gz"
    if [ "x${BRS}" != "x" ]; then
        echo "	./build.sh root-sdk var-sdk packages smart install -y $BRS"
    fi
    echo "	./build.sh root-sdk var-sdk packages rpmbuild -ba $spec"
    echo
    echo "`basename ${spec} .spec`: $PACKAGES"
    echo
done

echo -e "sources: $ALL_SOURCES"
