NAME          = am-packbuild
PACKAGE	      ?= archivematica
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID ?= 0F4A4D31
PACKBUILD_EXTRA_ARGS ?= 
#PACKBUILD_EXTRA_ARGS ?= "-b 1"
PACKAGE = archivematica-storage-service
BRANCH     ?= stable/0.11.x
VERSION     ?= 0.11.0
RELEASE       ?= +rc2~xenial
BUILD_TYPE         ?= ss

.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image deb-clean build

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
                -e BUILD_TYPE=$(BUILD_TYPE) \
                -e GPG_ID=$(GPG_ID) \
		-e GPG_KEY \
		-e PACKBUILD_EXTRA_ARGS="$(PACKBUILD_EXTRA_ARGS)" \
 		--rm \
                --volume "$(shell cd ../../ && pwd):$(DEB_TOPDIR)/$(NAME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		 $(DOCKER_IMAGE) \
                 make -C $(DOCKER_VOLUME) deb-build

deb-build: 
	@echo "==> Install dependencies."
	# Add GPG if available
	@if [ -f "$(DOCKER_VOLUME)/GPG-KEY" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEY; fi
	@if [ x"$$GPG_KEY" != x ]; then echo "$$GPG_KEY" | gpg --import - ; fi
	#@cd /debbuild/$(NAME) && ./packbuild.py -r $(BUILD_TYPE) -v $(VERSION) -c $(BRANCH) -k$(GPG_ID) $(PACKBUILD_EXTRA_ARGS) 
	@cd /debbuild/$(NAME)  
	@echo "==> Clone code."
	./build.sh
	mkdir -p repo/
	cp -rf src/archivematica-*.* repo
	cd  repo && dpkg-scanpackages . | gzip > Packages.gz

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/
	mkdir -p src/$(PACKAGE)
	sudo rm -rf src/
	@git clone \
	  --quiet \
 	  --branch $(BRANCH) \
 	  --depth 1 \
          --single-branch \
  	  --recurse-submodules \
    		https://github.com/artefactual/$(PACKAGE)\
     	  src/$(PACKAGE) 
	cd src/$(PACKAGE) && git submodule init && \
		git submodule update 

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
