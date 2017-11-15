NAME          = am-packbuild
PACKAGE	      ?= archivematica
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID ?= 0F4A4D31
PACKBUILD_EXTRA_ARGS ?= 
#PACKBUILD_EXTRA_ARGS ?= "-b 1"
BRANCH     ?= qa/1.x
VERSION     ?= 1.7.0
RELEASE       ?= rc1
BUILD_TYPE         ?= am

.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image build

build-docker-image: update-changelog
	@echo "==> Building Docker image with build environment."
	@docker build --no-cache --rm --tag "$(DOCKER_IMAGE)" .

build:
	@echo "==> Building deb."
	@docker run \
                -e BRANCH=$(BRANCH) \
		-e VERSION=$(VERSION) \
		-e RELEASE=$(RELEASE) \
                -e BUILD_TYPE=$(BUILD_TYPE) \
                -e GPG_ID=$(GPG_ID) \
		-e GPG_KEY \
		-e PACKBUILD_EXTRA_ARGS="$(PACKBUILD_EXTRA_ARGS)" \
 		--rm \
                --volume "$(shell cd ../../ && pwd):$(DEB_TOPDIR)/$(NAME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
                 make -C $(DOCKER_VOLUME) deb-build

dev:
	@echo "==> Building deb."
	@docker run -i -t \
                -e BRANCH=$(BRANCH) \
		-e VERSION=$(VERSION) \
		-e RELEASE=$(RELEASE) \
                -e BUILD_TYPE=$(BUILD_TYPE) \
                -e GPG_ID=$(GPG_ID) \
		-e GPG_KEY \
		-e PACKBUILD_EXTRA_ARGS="$(PACKBUILD_EXTRA_ARGS)" \
 		--rm \
                --volume "$(shell cd ../../ && pwd):$(DEB_TOPDIR)/$(NAME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
                 /bin/bash


deb-build: deb-clean
	@echo "==> Install dependencies."
	# Add GPG if available
	@if [ -f "$(DOCKER_VOLUME)/GPG-KEY" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEY; fi
	@if [ x"$$GPG_KEY" != x ]; then echo "$$GPG_KEY" | gpg --import - ; fi
	#@cd /debbuild/$(NAME) && ./packbuild.py -r $(BUILD_TYPE) -v $(VERSION) -c $(BRANCH) -k$(GPG_ID) $(PACKBUILD_EXTRA_ARGS) 
	@cd /debbuild/$(NAME)  
	@echo "==> Clone code."
	mkdir -p src/$(PACKAGE)
	rm -rf src/
	@git clone \
	  --quiet \
 	  --branch $(BRANCH) \
 	  --depth 1 \
          --single-branch \
  	  --recurse-submodules \
    		https://github.com/artefactual/$(PACKAGE)\
	  src/$(PACKAGE) 
	cd src/$(PACKAGE) && git submodule init && \
		git submodule update && \
		cd ../../	
	./build.sh
	mkdir -p repo/
	cp -rf src/archivematica/src/archivematica-* repo
	cd  repo && dpkg-scanpackages . | gzip > Packages.gz

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
