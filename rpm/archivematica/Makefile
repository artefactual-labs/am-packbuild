PACKAGE     ?= archivematica
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  ?= "rpmbuild-$(PACKAGE)-$(VERSION)"

BRANCH     ?= stable/1.7.x
VERSION     ?= 1.7.0
RELEASE       ?= rc1

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "_etcdir $(DOCKER_VOLUME)/etc" \
	--define "_branch $(BRANCH)" \
	--define "name $(PACKAGE)" \
	--define "rpmversion $(VERSION)" \
	--define "rpmrelease $(RELEASE)" \
	--define "branch $(BRANCH)"

.PHONY: build-docker-image build rpm-build rpm-clean rpm-test

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" .

build:
	@echo "==> Building RPM."
	@docker run \
                -e RPM_TOPDIR="$(RPM_TOPDIR)" \
		-e DOCKER_VOLUME="$(DOCKER_VOLUME)/etc" \
		-e PACKAGE="$(PACKAGE)" \
		-e VERSION="$(VERSION)" \
		-e RELEASE="$(RELEASE)" \
		-e BRANCH="$(BRANCH)" \
		--rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) rpm-build

dev:
	@echo "==> Building RPM."
	@docker run -i -t \
                -e RPM_TOPDIR="$(RPM_TOPDIR)" \
		-e DOCKER_VOLUME="$(DOCKER_VOLUME)/etc" \
		-e PACKAGE="$(PACKAGE)" \
		-e VERSION="$(VERSION)" \
		-e RELEASE="$(RELEASE)" \
		-e BRANCH="$(BRANCH)" \
		--rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) /bin/bash

cleanup:
	@echo "==> Remove artifacts created as root."
	@docker run -i  \
		--rm \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		 $(DOCKER_IMAGE) \
		bash -c "rm -rf /src/*.rpm"


rpm-build: rpm-clean
	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)
	cp $(DOCKER_VOLUME)/$(PACKAGE).spec $(RPM_TOPDIR)/package.spec
	yum-builddep -y $(RPM_TOPDIR)/package.spec
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec

	@echo "==> Copying RPM files."
	cp -p $(RPM_TOPDIR)/RPMS/x86_64/$(PACKAGE)-*.x86_64.rpm $(DOCKER_VOLUME)
	cp -p $(RPM_TOPDIR)/SRPMS/$(PACKAGE)-*.src.rpm $(DOCKER_VOLUME)

rpm-clean:
	@echo "==> Cleaning up previous builds."
	@rm -rf $(RPM_TOPDIR)

rpm-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" centos:7 bash -c "yum install -y epel-release && yum localinstall -y --nogpgcheck $(DOCKER_VOLUME)/$(PACKAGE)-$(VERSION)*.rpm"
