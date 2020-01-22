NAME          = cadence-web
VERSION       ?= 3.4.1
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "name $(NAME)" \
	--define "version $(VERSION)"

.PHONY: build-docker-image build rpm-build rpm-clean rpm-test

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "${DOCKER_IMAGE}" .

build:
	@echo "==> Building RPM inside Docker container."
	@docker run --rm -e VERSION="$(VERSION)" \
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

rpm-build: rpm-clean
	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/{BUILD,RPMS,SRPMS}
	mkdir -p $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)
	wget -q https://codeload.github.com/uber/cadence-web/tar.gz/${VERSION} -O $(RPM_TOPDIR)/SOURCES/cadence-web-${VERSION}.tar.gz
	cd $(RPM_TOPDIR)/SOURCES/ && tar zxf cadence-web-${VERSION}.tar.gz
	cp $(DOCKER_VOLUME)/files/cadence-web.service $(RPM_TOPDIR)/SOURCES/
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
