#!/bin/bash -x

BASE="$(pwd)"
SOURCE=${BASE}/src/archivematica/src/
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"

cd $SOURCE
BRANCH="$(git branch | cut -d\  -f2-)"
COMMIT=$(git rev-parse HEAD)


# Update changelog for xenial
for i in dashboard MCPClient MCPServer archivematicaCommon
	do
	cd "${SOURCE}/$i/"
	dch -v 1:${VERSION}${RELEASE} commit: $(echo $COMMIT)
	dch -v 1:${VERSION}${RELEASE} checkout: $(echo $BRANCH) 
	dch -r --distribution xenial --urgency high ignored		
	cp $BASE/debian-$i/* debian/
	QUILT_PATCHES="debian/patches" quilt push -a || true
	dpkg-buildpackage -us -uc
	cd $SOURCE
	done

