#!/usr/bin/env bash

set -euxo pipefail

BASE="$(pwd)"
SOURCE="${BASE}/src/archivematica"
export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"
export DEB_BUILD_OPTIONS="noddebs"

clean_build_deps_artifacts() {
	find . -maxdepth 1 -type f -name "*build-deps*.*" -delete
}

# Create archivematica package.
pushd "${SOURCE}"
COMMIT=$(git rev-parse HEAD)
cp -rf "${BASE}/debian-archivematica" debian
mk-build-deps -i debian/control
clean_build_deps_artifacts
dch -v "1:${VERSION}${RELEASE}~24.04" "commit: ${COMMIT}"
dch -v "1:${VERSION}${RELEASE}~24.04" "checkout: ${BRANCH}"
dch -r --distribution noble --urgency high ignored
dpkg-buildpackage -us -uc
popd

# Create child packages.
for i in dashboard MCPClient MCPServer archivematicaCommon; do
	pushd "${SOURCE}/src/archivematica/${i}"
	cp -rf "${BASE}/debian-${i}" debian
	mk-build-deps -i debian/control
	clean_build_deps_artifacts
	dch -v "1:${VERSION}${RELEASE}~24.04" "commit: ${COMMIT}"
	dch -v "1:${VERSION}${RELEASE}~24.04" "checkout: ${BRANCH}"
	dch -r --distribution noble --urgency high ignored
	dpkg-buildpackage -us -uc
	popd
done
