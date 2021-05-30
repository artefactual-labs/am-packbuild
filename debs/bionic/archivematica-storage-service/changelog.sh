#!/usr/bin/env bash

export DEBFULLNAME="Artefactual Systems"
export DEBEMAIL="sysadmin@artefactual.com"
BRANCH="$(git branch | cut -d\  -f2-)"
COMMIT=$(git rev-parse HEAD)

dch -v 1:${VERSION}${RELEASE} commit: $(echo $COMMIT)
dch -v 1:${VERSION}${RELEASE} checkout: $(echo $BRANCH) 
dch -r --distribution bionic --urgency high ignored
