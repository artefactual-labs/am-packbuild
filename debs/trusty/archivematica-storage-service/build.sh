#!/bin/bash -x

BASE="$(pwd)"
SOURCE=${BASE}/src/archivematica-storage-service/
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"

cd $SOURCE
COMMIT=$(git rev-parse HEAD)
cp -rf ${BASE}/debian-storage-service/* debian/
yes | mk-build-deps -i debian/control
pip download -d lib --no-binary :all: -r requirements.txt
dch -v 1:${VERSION}${RELEASE} commit: $(echo $COMMIT)
dch -v 1:${VERSION}${RELEASE} checkout: $(echo $BRANCH) 
dch -r --distribution trusty --urgency high ignored
QUILT_PATCHES="debian/patches" quilt push -a || true
dpkg-buildpackage -us -uc
cd $SOURCE

