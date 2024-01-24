NAME          = temporal-ui-server
VERSION       ?= 2.20.0
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"
TEMPORAL_UI_SRC_DIR = "/go/src/github.com/temporalio/ui-server"

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
	@echo "==> Downloading temporal ui-server."
	mkdir -p $(TEMPORAL_UI_SRC_DIR)
	git clone --branch v$(VERSION) --depth 1 https://github.com/temporalio/ui-server.git $(TEMPORAL_UI_SRC_DIR)

	@echo "==> Building sources."
	go build -C $(TEMPORAL_UI_SRC_DIR) -o temporal-ui cmd/server/main.go


	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/{BUILD,RPMS,SRPMS}
	mkdir -p $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)
	cp -pR $(TEMPORAL_UI_SRC_DIR)/* $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)/
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
