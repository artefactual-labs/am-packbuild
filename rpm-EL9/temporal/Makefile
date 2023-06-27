NAME          = temporal
VERSION       ?= 1.21.1
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"
TEMPORAL_SRC_DIR = "/go/src/github.com/temporalio/temporal"
TEMPORAL_BIN_TARBALL = "https://github.com/temporalio/temporal/releases/download/v$(VERSION)/$(NAME)_$(VERSION)_linux_amd64.tar.gz"
TEMPORAL_SRC_TARBALL = "https://github.com/temporalio/temporal/archive/refs/tags/v$(VERSION).tar.gz"

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
	@docker run --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) rpm-build

rpm-build: rpm-clean
	@echo "==> Downloading temporal binaries and sources."
	mkdir -p $(TEMPORAL_SRC_DIR)
	wget -q -O $(TEMPORAL_SRC_DIR)/$(NAME)_$(VERSION)_linux_amd64.tar.gz $(TEMPORAL_BIN_TARBALL)
	wget -q -O $(TEMPORAL_SRC_DIR)/v$(VERSION).tar.gz $(TEMPORAL_SRC_TARBALL)

	@echo "==> Unpacking tarballs and selecting desired files/dir"
	tar xfz $(TEMPORAL_SRC_DIR)/$(NAME)_$(VERSION)_linux_amd64.tar.gz -C $(TEMPORAL_SRC_DIR)/
	tar xfz $(TEMPORAL_SRC_DIR)/v$(VERSION).tar.gz --directory $(TEMPORAL_SRC_DIR)/
	cp -a $(TEMPORAL_SRC_DIR)/temporal-$(VERSION)/schema $(TEMPORAL_SRC_DIR)/
	rm -rf $(TEMPORAL_SRC_DIR)/*tar.gz $(TEMPORAL_SRC_DIR)/temporal-$(VERSION) $(TEMPORAL_SRC_DIR)/config

	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/{BUILD,RPMS,SRPMS}
	mkdir -p $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)
	cp -pR $(TEMPORAL_SRC_DIR)/* $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)/
	cp -pR files/* $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)/
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
	docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" rockylinux:9 bash -c "rpm -i $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm && sf -version"
