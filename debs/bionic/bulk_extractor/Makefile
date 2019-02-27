NAME          = bulk_extractor
VERSION       ?= 1.5.5
RELEASE	      ?= 1~18.04
SRC_URL       = http://downloads.digitalcorpora.org/downloads/bulk_extractor/bulk_extractor-1.5.5.tar.gz
SRC_SHA256    = 297a57808c12b81b8e0d82222cf57245ad988804ab467eb0a70cf8669594e8ed
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"

.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" --build-arg SRC_URL="$(SRC_URL)" --build-arg SRC_VERSION="$(VERSION)" --build-arg SRC_SHA256="$(SRC_SHA256)" --build-arg PACKAGE="$(NAME)" .

update-changelog:
	@echo "==> Update changelog."
	@dch -v $(VERSION)-$(RELEASE) -D bionic "New upstream release"

build:
	@echo "==> Building deb."
	@docker run --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build: deb-clean
	@echo "==> Install dependencies."
	cd /debbuild/$(NAME) && yes | mk-build-deps --install debian/control
	@echo "==> Update changelog."
	cd /debbuild/$(NAME) && dch -v $(VERSION)-$(RELEASE) -D bionic "New upstream release"

	@echo "==> Run bootstrap.sh."
	cd /debbuild/$(NAME) && sh bootstrap.sh
	@echo "==> Build package."
	cd /debbuild/$(NAME) && dpkg-buildpackage 
	@echo "==> Copying built  files."
	mkdir -p $(DOCKER_VOLUME)/build/
	cp  $(DEB_TOPDIR)/*.*  $(DOCKER_VOLUME)/build/ 

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/

# TODO: Create repo and test it
deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
