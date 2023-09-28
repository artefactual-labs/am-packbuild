NAME          = tctl
VERSION       ?= 1.18.0
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"
TCTL_SRC = "/go/src/github.com/temporalio/tctl"

CHANGELOG_DATE = $(shell date "+%a %b %d %Y")
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
	@echo "==> Download and unpack tctl."
	mkdir -p $(TCTL_SRC)
	wget -q https://github.com/temporalio/tctl/releases/download/v${VERSION}/tctl_${VERSION}_linux_amd64.tar.gz -O $(TCTL_SRC)/tctl.tar.gz
	cd $(TCTL_SRC) && tar zxf tctl.tar.gz


	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/{BUILD,RPMS,SRPMS}
	mkdir -p $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)
	cp -p $(TCTL_SRC)/tctl $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)/
	cp -p $(TCTL_SRC)/tctl-authorization-plugin $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)/
	tar czf $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION).tar.gz -C $(RPM_TOPDIR)/SOURCES $(NAME)-$(VERSION)
	sed -i '2s/^/* $(CHANGELOG_DATE) Artefactual <sysadmin@artefactual.com> - $(VERSION)\n- Changes: Added v$(VERSION) version\n/' $(DOCKER_VOLUME)/changelog
	cp $(DOCKER_VOLUME)/package.spec $(RPM_TOPDIR)/package.spec
	cat $(DOCKER_VOLUME)/changelog >> $(RPM_TOPDIR)/package.spec

	@echo "==> Running rpmbuild."
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec

	@echo "==> Copying RPM files."
	cp -p $(RPM_TOPDIR)/RPMS/x86_64/$(NAME)-$(VERSION)*.x86_64.rpm $(DOCKER_VOLUME)/
	cp -p $(RPM_TOPDIR)/SRPMS/$(NAME)-$(VERSION)*.src.rpm $(DOCKER_VOLUME)/

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)

rpm-test:
	docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" rockylinux:9 bash -c "rpm -i $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm && sf -version"
