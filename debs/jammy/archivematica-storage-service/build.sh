#!/usr/bin/env bash

set -euxo pipefail

BASE="$(pwd)"
SOURCE="${BASE}/src/archivematica-storage-service/"
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"
export DEB_BUILD_OPTIONS="noddebs"

cd "$SOURCE"
COMMIT=$(git rev-parse HEAD)
cp -rf "${BASE}/debian-storage-service" debian
mk-build-deps -i debian/control
find . -maxdepth 1 -type f -name "*build-deps*.*" -delete
dch -v "1:${VERSION}${RELEASE}~22.04" "commit: ${COMMIT}"
dch -v "1:${VERSION}${RELEASE}~22.04" "checkout: ${BRANCH}"
dch -r --distribution jammy --urgency high ignored
dpkg-buildpackage -us -uc
cd "$SOURCE"
