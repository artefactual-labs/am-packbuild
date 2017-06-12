NAME          = am-packbuild
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID ?= 0F4A4D31
PACKBUILD_EXTRA_ARGS ?= 
#PACKBUILD_EXTRA_ARGS ?= "-b 1"
CURRENT_DIR=$(shell basename `pwd`)


ifeq ($(CURRENT_DIR),archivematica)
BRANCH     ?= stable/1.6.x
VERSION     ?= 1.6.0
RELEASE       ?= 1
PACKAGE         ?= am
else 
BRANCH     ?= stable/0.10.x
VERSION     ?= 0.10.0
RELEASE       ?= 1
PACKAGE         ?= ss
endif

.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image build

build-docker-image: update-changelog
	@echo "==> Building Docker image with build environment."
	@docker build --rm --tag "$(DOCKER_IMAGE)" .

build:
	@echo "==> Building deb."
	@docker run \
                -e BRANCH=$(BRANCH) \
		-e VERSION=$(VERSION) \
		-e RELEASE=$(RELEASE) \
                -e PACKAGE=$(PACKAGE) \
                -e GPG_ID=$(GPG_ID) \
		-e PACKBUILD_EXTRA_ARGS="$(PACKBUILD_EXTRA_ARGS)" \
 		--rm \
                --volume "$(shell cd ../../ && pwd):$(DEB_TOPDIR)/$(NAME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
                 make -C $(DOCKER_VOLUME) deb-build

deb-build: deb-clean
	@echo "==> Install dependencies."
	# Add GPG if available
	@if [ -f "$(DOCKER_VOLUME)/GPG-KEY" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEY; fi
	@cd /debbuild/$(NAME) && ./packbuild.py -r $(PACKAGE) -v $(VERSION) -c $(BRANCH) -k$(GPG_ID) $(PACKBUILD_EXTRA_ARGS) 
	@echo "==> Copying deb files."
	mkdir -p $(DOCKER_VOLUME)/build/
	cp -rf /tmp/ampackbuilder/* $(DOCKER_VOLUME)/build/
	cd $(DOCKER_VOLUME)/build/ && dpkg-scanpackages . | gzip > Packages.gz

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
