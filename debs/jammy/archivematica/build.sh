#!/usr/bin/env bash

set -euxo

BASE="$(pwd)"
SOURCE=${BASE}/src/archivematica
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"
export DEB_BUILD_OPTIONS="noddebs"

# Create archivematica package.
pushd ${SOURCE}
COMMIT=$(git rev-parse HEAD)
cp -rf ${BASE}/debian-archivematica debian
yes | mk-build-deps -i debian/control
dch -v 1:${VERSION}${RELEASE}~22.04 commit: $(echo $COMMIT)
dch -v 1:${VERSION}${RELEASE}~22.04 checkout: $(echo $BRANCH)
dch -r --distribution jammy --urgency high ignored
dpkg-buildpackage -us -uc
popd

# Install front-end node modules.
pushd $SOURCE/src/dashboard/frontend/
npm install --unsafe-perm
popd

# Create child packages.
for i in dashboard MCPClient MCPServer archivematicaCommon; do
	pushd "${SOURCE}/src/$i"
	cp -rf $BASE/debian-$i debian
	yes | mk-build-deps -i debian/control
	dch -v 1:${VERSION}${RELEASE}~22.04 commit: $(echo $COMMIT)
	dch -v 1:${VERSION}${RELEASE}~22.04 checkout: $(echo $BRANCH)
	dch -r --distribution jammy --urgency high ignored
	dpkg-buildpackage -us -uc
	popd
done
