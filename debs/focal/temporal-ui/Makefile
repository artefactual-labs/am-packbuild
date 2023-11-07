NAME          = temporal-ui
PACKAGE       = temporal-ui
VERSION       ?= 2.20.0
RELEASE       ?= 1~$(DISTRO_CODENAME)
BRANCH        ?= v2.20.0
GIT_URL       = https://github.com/temporalio/ui-server.git
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID        ?= 486650CDD6355E25DA542E06C8F04D025236CA08
DISTRO_CODENAME = focal
.PHONY: build-docker-image build deb-build deb-clean deb-test

all: build-docker-image get-code build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --rm --tag "$(DOCKER_IMAGE)"  .

build:
	@echo "==> Building deb."
	@docker run --rm \
			-e BRANCH=$(BRANCH) \
			-e GIT_URL=$(GIT_URL) \
				-e VERSION=$(VERSION) \
				-e RELEASE=$(RELEASE) \
				-e BUILD_TYPE=$(BUILD_TYPE) \
				-e GPG_ID=$(GPG_ID) \
				-e GPG_KEY \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build:
	@echo "==> Install gpg keys."
	@if [ -f "$(DOCKER_VOLUME)/GPG-KEY" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEY; fi
	@if [ x"$$GPG_KEY" != x ]; then echo "$$GPG_KEY" | gpg --import - ; fi
	@echo "==> Clone code"
	# Update debian/folder and changelog, and install dependencies
	@cp debian src/$(PACKAGE) -rf
	@cd src/$(PACKAGE) && \
	dch -v ${VERSION}-${RELEASE} Commit $(shell cat src/$(PACKAGE)/.git/HEAD) && \
	dch -r --distribution $(DISTRO_CODENAME) --urgency medium ignored && \
	yes | mk-build-deps --install debian/control
	@echo "==> Build ui-server binary"
	cd src/$(PACKAGE) && go build -o ui-server ./cmd/server/main.go
	@echo "==> Build package."
	cd src/$(PACKAGE) && dpkg-buildpackage -k${GPG_ID}
	@echo "==> Copying DEB files."
	mkdir -p build
	cp src/$(PACKAGE)_* build/

get-code:
	@echo "==> Get code."
	@mkdir -p src/
	@docker run --rm \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) rm -rf $(DOCKER_VOLUME)/src/$(PACKAGE)
	@git clone \
			--quiet \
			--branch ${BRANCH} \
			--recurse-submodules $(GIT_URL) \
		src/$(PACKAGE)
	@echo "==> Copy systemd and config file to src dir"
	@cp files/* src/$(PACKAGE)

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:$(DISTRO_CODENAME) echo "Create repo and install package"
