NAME          = siegfried
PACKAGE       = siegfried
VERSION       ?= 1.11.5
RELEASE       ?= 1
BRANCH        ?= v1.11.5
GIT_URL       = https://github.com/richardlehane/siegfried/
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID        ?= 0F4A4D31
DISTRO_CODENAME = xenial
GOOS          ?= linux
GOARCH        ?= amd64
.PHONY: build-docker-image build deb-build deb-clean deb-test

all: build-docker-image get-code build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --rm --build-arg GOOS=$(GOOS) --build-arg GOARCH=$(GOARCH) --tag "$(DOCKER_IMAGE)"  .

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
				-e GOOS=$(GOOS) \
				-e GOARCH=$(GOARCH) \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build:
	@echo "==> Install gpg keys."
	@if [ -f "$(DOCKER_VOLUME)/GPG-KEY" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEY; fi
	@if [ x"$$GPG_KEY" != x ]; then echo "$$GPG_KEY" | gpg --import - ; fi
	@echo "==> Prepare isolated build workspace."
	@WORKDIR="/tmp/build-$(PACKAGE)"; \
	rm -rf "$$WORKDIR" && mkdir -p "$$WORKDIR" && \
	echo "==> Clone code" && \
	cp -a src/$(PACKAGE) "$$WORKDIR"/ && \
	cp -a debian "$$WORKDIR"/$(PACKAGE)/ && \
	echo "==> Update changelog and install build-deps" && \
	cd "$$WORKDIR/$(PACKAGE)" && \
	dch -v ${VERSION}-${RELEASE} Commit $(shell cat src/$(PACKAGE)/.git/HEAD) && \
	dch -r --distribution $(DISTRO_CODENAME) --urgency medium ignored && \
	yes | mk-build-deps --install debian/control && \
	echo "==> Build package." && \
	PATH=${PATH} GOPATH=${GOPATH} dpkg-buildpackage -k${GPG_ID} && \
	echo "==> Copying DEB files." && \
	mkdir -p "$(DOCKER_VOLUME)/build" && \
	cp "$$WORKDIR"/$(PACKAGE)_* "$(DOCKER_VOLUME)/build/"

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

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:$(DISTRO_CODENAME) echo "Create repo and install package"
