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

all: build-docker-image build

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

deb-build: deb-clean
	@echo "==> Install gpg keys."
	@if [ -f "$(DOCKER_VOLUME)/GPG-KEY" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEY; fi
	@if [ x"$$GPG_KEY" != x ]; then echo "$$GPG_KEY" | gpg --import - ; fi
	@echo "==> Clone code"
	@echo nomkdir -p /debbuild/$(NAME)
	@echo nocd /debbuild/$(NAME)
	@mkdir -p src/
	rm -rf src/$(PACKAGE)
	git clone \
          --quiet \
          --branch ${BRANCH} \
          --recurse-submodules $(GIT_URL) \
	  src/$(PACKAGE)
	# Update debian/folder and changelog, and install dependencies
	# TODO: Debug problems when passing vars from command line
	@cp debian src/$(PACKAGE) -rf
	git --git-dir=/src/src/siegfried/.git rev-parse HEAD
	COMMIT=$(shell git --git-dir=/src/src/siegfried/.git rev-parse HEAD)
	@cd src/$(PACKAGE) && \
	dch -v ${VERSION}-${RELEASE} Commit $(shell cat /src/src/$(PACKAGE)/.git/HEAD) && \
	dch -r --distribution trusty --urgency medium ignored && \
	yes | mk-build-deps --install debian/control 
	@echo "==> Build package."
	cd src/$(PACKAGE) && PATH=/usr/lib/go-1.7/bin:${PATH} GOPATH=/usr/share/go-1.7/ dpkg-buildpackage  -k${GPG_ID}
	@echo "==> Copying DEB files."
	mkdir -p repo
	cp src/$(PACKAGE)_* repo/

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	#@rm -rf $(DEB_TOPDIR)

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
