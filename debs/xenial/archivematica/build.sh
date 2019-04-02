#!/bin/bash -x

BASE="$(pwd)"
SOURCE=${BASE}/src/archivematica/src/
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"

cd $SOURCE/dashboard/frontend/
npm install --unsafe-perm

cd $SOURCE
COMMIT=$(git rev-parse HEAD)

# Update changelog for xenial
for i in dashboard MCPClient MCPServer archivematicaCommon
	do
	cd "${SOURCE}/$i/"
	cp -rf $BASE/debian-$i debian
	yes | mk-build-deps -i debian/control
	dch -v 1:${VERSION}${RELEASE}~16.04 commit: $(echo $COMMIT)
	dch -v 1:${VERSION}${RELEASE}~16.04 checkout: $(echo $BRANCH) 
	dch -r --distribution xenial --urgency high ignored		
	QUILT_PATCHES="debian/patches" quilt push -a || true
	dpkg-buildpackage -us -uc
	cd $SOURCE
	done

