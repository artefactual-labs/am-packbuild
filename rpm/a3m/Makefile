NAME          = a3m
BRANCH        ?= master
VERSION       ?= 0.3.0
RELEASE       ?= 1
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = $(subst ~,-,"rpmbuild-$(NAME)-$(VERSION)")

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "_etcdir $(DOCKER_VOLUME)/etc" \
	--define "_branch $(BRANCH)" \
	--define "name $(NAME)" \
	--define "rpmversion $(VERSION)" \
	--define "rpmrelease $(RELEASE)"

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
                -e PACKAGE="$(NAME)" \
                -e VERSION="$(VERSION)" \
                -e RELEASE="$(RELEASE)" \
                -e BRANCH="$(BRANCH)" \
		--rm --volume "$(shell pwd):/$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C /src rpm-build

dev:
	@echo "==> Building RPM."
	@docker run -i -t \
                -e RPM_TOPDIR="$(RPM_TOPDIR)" \
                -e DOCKER_VOLUME="$(DOCKER_VOLUME)/etc" \
                -e PACKAGE="$(NAME)" \
                -e VERSION="$(VERSION)" \
                -e RELEASE="$(RELEASE)" \
                -e BRANCH="$(BRANCH)" \
		--rm --volume "$(shell pwd):/$(DOCKER_VOLUME)" $(DOCKER_IMAGE) /bin/bash


rpm-build: rpm-clean
	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)
	cp $(DOCKER_VOLUME)/package.spec $(RPM_TOPDIR)/package.spec
	#yum-builddep -y $(RPM_TOPDIR)/package.spec
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec

	@echo "==> Copying RPM files."
	cp -p $(RPM_TOPDIR)/RPMS/x86_64/$(NAME)-$(VERSION)*.x86_64.rpm $(DOCKER_VOLUME)
	cp -p $(RPM_TOPDIR)/SRPMS/$(NAME)-$(VERSION)*.src.rpm $(DOCKER_VOLUME)

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)

cleanup:
	@echo "==> Remove artifacts created as root."
	@docker run -i  \
		--rm \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
		bash -c "rm -rf /src/*.rpm"

rpm-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" centos:7 bash -c "yum install -y epel-release && yum localinstall -y --nogpgcheck $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm"
