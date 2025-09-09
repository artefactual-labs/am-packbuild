NAME          = bulk_extractor
UPSTREAM_NAME = bulk_extractor
VERSION       = 2.1.1
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "name $(NAME)" \
	--define "version $(VERSION)"

.PHONY: build-docker-image build rpm-build rpm-clean rpm-test cleanup

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" .

build:
	@echo "==> Building RPM."
	@docker run --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) rpm-build

rpm-build: rpm-clean
	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/SOURCES
	cp $(DOCKER_VOLUME)/package.spec $(RPM_TOPDIR)/
	@echo "==> Downloading source tarball."
	curl -Ls https://github.com/simsong/$(UPSTREAM_NAME)/releases/download/v$(VERSION)/$(UPSTREAM_NAME)-$(VERSION).tar.gz > $(RPM_TOPDIR)/SOURCES/$(UPSTREAM_NAME)-$(VERSION).tar.gz
	@echo "==> Running rpmbuild."
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec
	@echo "==> Copying RPM files."
	cp -t $(DOCKER_VOLUME) $(RPM_TOPDIR)/RPMS/*/$(NAME)-$(VERSION)*.rpm
	cp -t $(DOCKER_VOLUME) $(RPM_TOPDIR)/SRPMS/$(NAME)-$(VERSION)*.src.rpm

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)

cleanup:
	@echo "==> Remove artifacts created as root."
	@docker run -i \
		--rm \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
		bash -c "rm -rf /src/*.rpm"

rpm-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" rockylinux:9 bash -c "set -euo pipefail; yum install -y epel-release >/dev/null && RPM=\$$(ls $(DOCKER_VOLUME)/$(NAME)-$(VERSION)-1.el9.*.rpm | head -n1) && yum localinstall -y --nogpgcheck \"\$${RPM}\" >/dev/null && bulk_extractor --version"
