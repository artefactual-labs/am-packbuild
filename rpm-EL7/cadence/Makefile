NAME          = cadence
VERSION       ?= 0.19.2
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"
CTID          ?=$(shell docker create ubercadence/server:${VERSION})
ENDURO_SRC = "/go/src/github.com/artefactual-labs/enduro"

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "name $(NAME)" \
	--define "version $(VERSION)"

.PHONY: build-docker-image build rpm-build rpm-clean rpm-test

all: build-docker-image extract build clean-docker-extracted-files

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "${DOCKER_IMAGE}" .

extract:
	@echo "==> Extract files from cadence docker image"
	docker cp ${CTID}:/usr/local/bin/cadence files/
	docker cp ${CTID}:/usr/local/bin/cadence-server files/
	docker cp ${CTID}:/usr/local/bin/cadence-sql-tool files/
	docker cp ${CTID}:/etc/cadence/schema/mysql/v57/cadence/versioned files/cadence-migrations
	docker cp ${CTID}:/etc/cadence/schema/mysql/v57/visibility/versioned files/visibility-migrations

build:
	@echo "==> Building RPM inside Docker container."
	@docker run --rm -e VERSION="$(VERSION)" \
		-e CTID="${CTID}" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
		make -C $(DOCKER_VOLUME) rpm-build

dev:
	@echo "==> Building RPM inside Docker container."
	@docker run -i -t --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) /bin/bash

cleanup:
	@echo "==> Remove artifacts created as root."
	@docker run -i  \
                --rm \
                --volume "$(shell pwd):$(DOCKER_VOLUME)" \
                $(DOCKER_IMAGE) \
                bash -c "rm -rf /src/*.rpm"

clean-docker-extracted-files:
	@echo "==> Cleaning extracted files from docker."
	rm -rf files/cadence \
		files/cadence-server \
		files/cadence-sql-tool \
		files/cadence-migrations \
		files/visibility-migrations

rpm-build: rpm-clean
	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/{BUILD,RPMS,SRPMS}
	mkdir -p $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)
	cp -rf -p $(DOCKER_VOLUME)/files/* $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)/
	tar czf $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION).tar.gz -C $(RPM_TOPDIR)/SOURCES $(NAME)-$(VERSION)
	cp $(DOCKER_VOLUME)/package.spec $(RPM_TOPDIR)/package.spec

	@echo "==> Running rpmbuild."
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec

	@echo "==> Copying RPM files."
	cp -p $(RPM_TOPDIR)/RPMS/x86_64/$(NAME)-$(VERSION)*.x86_64.rpm $(DOCKER_VOLUME)/
	cp -p $(RPM_TOPDIR)/SRPMS/$(NAME)-$(VERSION)*.src.rpm $(DOCKER_VOLUME)/

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)

rpm-test:
	docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" centos:7 bash -c "rpm -i $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm && sf -version"
