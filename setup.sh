#!/bin/sh

mkdir -p packages/RPMS/noarch
mkdir -p packages/RPMS/x86_64

./setup_root.sh $1
./build.sh smart channel -y --add mydb type=rpm-sys name="RPM Database"
./build.sh smart channel -y --add noarch type=rpm-dir name="RPM Database" path=/self/packages/RPMS/noarch
./build.sh smart channel -y --add x86_64 type=rpm-dir name="RPM Database" path=/self/packages/RPMS/x86_64/
