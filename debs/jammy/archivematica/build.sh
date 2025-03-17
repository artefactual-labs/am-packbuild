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

update_install_file() {
	local i="$1"
	local target_dir="/usr/lib/archivematica/$i/"

	case "$i" in
		dashboard)
			install_file="archivematica-dashboard.install"
			target_dir="/usr/share/archivematica/$i/"
			;;
		MCPClient)
			install_file="archivematica-mcp-client.install"
			;;
		MCPServer)
			install_file="archivematica-mcp-server.install"
			;;
		archivematicaCommon)
			install_file="archivematica-common.install"
			;;
	esac

	# List all non-hidden files and directories in the current directory,
	# excluding 'install' and 'debian', and append their names along with the
	# designated target directory to the install file.
	find . -maxdepth 1 \( -type f -o -type d \) -not -name ".*" -not -path "./install" -not -path "./debian" -exec echo "{} $target_dir" \; >> "debian/$install_file"
}

# Create child packages.
for i in dashboard MCPClient MCPServer archivematicaCommon; do
	pushd "${SOURCE}/src/$i"
	cp -rf $BASE/debian-$i debian
	update_install_file "$i"
	yes | mk-build-deps -i debian/control
	dch -v 1:${VERSION}${RELEASE}~22.04 commit: $(echo $COMMIT)
	dch -v 1:${VERSION}${RELEASE}~22.04 checkout: $(echo $BRANCH)
	dch -r --distribution jammy --urgency high ignored
	dpkg-buildpackage -us -uc
	popd
done
