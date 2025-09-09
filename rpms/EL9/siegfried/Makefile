NAME          = siegfried
VERSION       = 1.11.2
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"
SIEGFRIED_SRC = "/go/src/github.com/richardlehane/siegfried"
GOOS          ?= linux
GOARCH        ?= amd64

RPM_ARCH = $(GOARCH)
ifeq ($(GOARCH),amd64)
  RPM_ARCH = x86_64
else ifeq ($(GOARCH),arm64)
  RPM_ARCH = aarch64
endif

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "name $(NAME)" \
	--define "version $(VERSION)" \
	--target "$(RPM_ARCH)"

.PHONY: build-docker-image build rpm-build rpm-clean rpm-test

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build \
		--build-arg GOOS=$(GOOS) \
		--build-arg GOARCH=$(GOARCH) \
		--tag "${DOCKER_IMAGE}" .

build:
	@echo "==> Building RPM inside Docker container."
	@docker run --rm \
		-e GOOS=$(GOOS) \
		-e GOARCH=$(GOARCH) \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) rpm-build

rpm-build: rpm-clean
	@echo "==> Downloading siegfried."
	mkdir -p $(SIEGFRIED_SRC)
	git clone --branch v$(VERSION) --depth 1 https://github.com/richardlehane/siegfried.git $(SIEGFRIED_SRC)
	cd $(SIEGFRIED_SRC)

	@echo "==> Building sources."
	GOOS=$(GOOS) GOARCH=$(GOARCH) go install -tags archivematica -v github.com/richardlehane/siegfried/cmd/sf@v$(VERSION)
	GOOS=$(GOOS) GOARCH=$(GOARCH) go install -tags archivematica -v github.com/richardlehane/siegfried/cmd/roy@v$(VERSION)

	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/{BUILD,RPMS,SRPMS}
	mkdir -p $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)
	cp /go/bin/* $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)/
	tar czf $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION).tar.gz -C $(RPM_TOPDIR)/SOURCES $(NAME)-$(VERSION)
	cp $(DOCKER_VOLUME)/package.spec $(RPM_TOPDIR)/package.spec

	@echo "==> Running rpmbuild."
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec

	@echo "==> Copying RPM files."
	cp $(RPM_TOPDIR)/RPMS/$(RPM_ARCH)/$(NAME)-$(VERSION)*.$(RPM_ARCH).rpm $(DOCKER_VOLUME)/
	cp $(RPM_TOPDIR)/SRPMS/$(NAME)-$(VERSION)*.src.rpm $(DOCKER_VOLUME)/

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
	docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" rockylinux:9 bash -c "rpm -i $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm && sf -version"
