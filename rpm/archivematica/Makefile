PACKAGE     ?= archivematica
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  ?= "rpmbuild-$(PACKAGE)-$(VERSION)"

ifeq ($(PACKAGE),archivematica)
BRANCH     ?= stable/1.6.x
VERSION     ?= 1.6.0
RELEASE       ?= 1
else
BRANCH     ?= stable/0.10.x
VERSION     ?= 0.10.0
RELEASE       ?= 1
endif

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "_etcdir $(DOCKER_VOLUME)/etc" \
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
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)

rpm-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" centos:7 bash -c "yum install -y epel-release && yum localinstall -y --nogpgcheck $(DOCKER_VOLUME)/$(PACKAGE)-$(VERSION)*.rpm"
