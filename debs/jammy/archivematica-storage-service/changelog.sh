#!/usr/bin/env bash

set -euxo pipefail

export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"
BRANCH="$(git branch | cut -d' ' -f2-)"
COMMIT=$(git rev-parse HEAD)

dch -v "1:${VERSION}${RELEASE}" "commit: ${COMMIT}"
dch -v "1:${VERSION}${RELEASE}" "checkout: ${BRANCH}"
dch -r --distribution jammy --urgency high ignored
