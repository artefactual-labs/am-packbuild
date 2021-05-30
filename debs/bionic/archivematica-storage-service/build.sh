#!/usr/bin/env bash

set -euxo

BASE="$(pwd)"
SOURCE=${BASE}/src/archivematica-storage-service/
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"
export DEB_BUILD_OPTIONS="noddebs"

cd $SOURCE
COMMIT=$(git rev-parse HEAD)
cp -rf ${BASE}/debian-storage-service debian
yes | mk-build-deps -i debian/control
dch -v 1:${VERSION}${RELEASE}~18.04 commit: $(echo $COMMIT)
dch -v 1:${VERSION}${RELEASE}~18.04 checkout: $(echo $BRANCH) 
dch -r --distribution bionic --urgency high ignored		
dpkg-buildpackage -us -uc
cd $SOURCE

