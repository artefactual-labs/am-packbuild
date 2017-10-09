#!/bin/bash -x

BASE="$(pwd)"
SOURCE=${BASE}/src/archivematica-storage-service/
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"

cd $SOURCE
BRANCH="$(git branch | cut -d\  -f2-)"
COMMIT=$(git rev-parse HEAD)
cp ${BASE}/debian-storage-service/* debian/
pip download -d lib --no-binary :all: -r requirements.txt
dch -v 1:${VERSION}${RELEASE} commit: $(echo $COMMIT)
dch -v 1:${VERSION}${RELEASE} checkout: $(echo $BRANCH) 
dch -r --distribution trusty --urgency high ignored		
dpkg-buildpackage -us -uc
cd $SOURCE

