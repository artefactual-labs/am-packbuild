#!/bin/bash -x

BASE="$(pwd)"
SOURCE=${BASE}/src/archivematica/src/
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"

for j in transfer-browser appraisal-tab
  do
    cd $SOURCE/dashboard/frontend/$j/
    npm install --unsafe-perm
  done

cd $SOURCE
COMMIT=$(git rev-parse HEAD)

# Just to be sure we use the correct pip
rm -f /usr/bin/pip /usr/bin/pip2

PATH=/usr/local/bin:$PATH
export DH_VIRTUALENV_INSTALL_ROOT=/usr/share/python/
# Update changelog for trusty
for i in dashboard MCPClient MCPServer archivematicaCommon
	do
	cd "${SOURCE}/$i/"
	cp -rf $BASE/debian-$i debian
	yes | mk-build-deps -i debian/control
	dch -v 1:${VERSION}${RELEASE} commit: $(echo $COMMIT)
	dch -v 1:${VERSION}${RELEASE} checkout: $(echo $BRANCH) 
	dch -r --distribution trusty --urgency high ignored		
	QUILT_PATCHES="debian/patches" quilt push -a || true
	dpkg-buildpackage -us -uc
	cd $SOURCE
	done

