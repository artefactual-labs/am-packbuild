NAME          = am-packbuild
AM_BRANCH     = dev/update-1.6-dependencies
AM_VERSION     = 1.6.0
RELEASE	      = 2
GIT_URL	      = https://github.com/artefactual-labs/am-packbuild
GIT_BRANCH    = dev/packaging-1.6
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(AM_VERSION)"

.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image build

build-docker-image: update-changelog
	@echo "==> Building Docker image with build environment."
	@docker build --rm --tag "$(DOCKER_IMAGE)" --build-arg GIT_URL="$(GIT_URL)" --build-arg GIT_BRANCH="$(GIT_BRANCH)" --build-arg PACKAGE="$(NAME)" .

build:
	@echo "==> Building deb."
	@docker run --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build: deb-clean
	@echo "==> Install dependencies."
	#cd /debbuild/$(NAME) && find . -iname control 
	cd /debbuild/$(NAME) && ./packbuild.py -r am -v $(AM_VERSION) -c $(AM_BRANCH) -k0F4A4D31
	@echo "==> Build package."
	#cd /debbuild/$(NAME) && dpkg-buildpackage -us -uc -k
	@echo "==> Copying RPM files."
	mkdir -p $(DOCKER_VOLUME)/build/
	cp /tmp/ampackbuilder/*/archivematica/src/*.* $(DOCKER_VOLUME)/build/

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
