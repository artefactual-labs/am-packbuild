#!/bin/bash -x

BASE="$(pwd)"
SOURCE=${BASE}/src/archivematica-storage-service/
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"

cd $SOURCE
COMMIT=$(git rev-parse HEAD)
cp -rf ${BASE}/debian-storage-service debian
QUILT_PATCHES="debian/patches" quilt push -a || true
pip download -d lib --no-binary :all: -r requirements.txt
yes | mk-build-deps -i debian/control
dch -v 1:${VERSION}${RELEASE}~16.04 commit: $(echo $COMMIT)
dch -v 1:${VERSION}${RELEASE}~16.04 checkout: $(echo $BRANCH) 
dch -r --distribution xenial --urgency high ignored		
dpkg-buildpackage -us -uc
cd $SOURCE

