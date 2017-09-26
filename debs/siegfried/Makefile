NAME          = siegfried
PACKAGE       = siegfried
VERSION       ?= 1.7.3
RELEASE	      ?= 1
BRANCH        ?= v1.7.3
GIT_URL	      = https://github.com/richardlehane/siegfried/
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID        ?= 0F4A4D31
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
	dch -r --distribution trusty --urgency medium ignored && \
	yes | mk-build-deps --install debian/control 
	@echo "==> Build package."
	cd src/$(PACKAGE) && PATH=/usr/lib/go-1.9/bin:${PATH} GOPATH=/usr/share/go-1.9/ dpkg-buildpackage  -k${GPG_ID}
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

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
