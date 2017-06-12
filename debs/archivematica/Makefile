NAME          = am-packbuild
AM_BRANCH     ?= stable/1.6.x
AM_VERSION     ?= 1.6.0
RELEASE	      ?= 1
GIT_URL	      = https://github.com/artefactual-labs/am-packbuild
GIT_BRANCH    = dev/packaging-1.6-docker
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(AM_VERSION)"
PACKBUILD_PARMS ?= 
#PACKBUILD_PARMS ?= "-b 1 -k05236CA08"
.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image build

build-docker-image: update-changelog
	@echo "==> Building Docker image with build environment."
	@docker build --rm --tag "$(DOCKER_IMAGE)" --build-arg GIT_URL="$(GIT_URL)" --build-arg GIT_BRANCH="$(GIT_BRANCH)" --build-arg PACKAGE="$(NAME)" .

                #--volume "$(shell cd ../../ && echo $(PWD))":/debbuild/am-packbuild \		
build:
	@echo "==> Building deb."
	@docker run \
                -e AM_BRANCH=$(AM_BRANCH) \
		-e AM_VERSION=$(AM_VERSION) \
		-e AM_RELEASE=$(AM_RELEASE) \
		-e PACKBUILD_PARMS="$(PACKBUILD_PARMS)" \
 		--rm \
                --volume "$(shell cd ../../ && pwd):$(DEB_TOPDIR)/$(NAME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
                 make -C $(DOCKER_VOLUME) deb-build

deb-build: deb-clean
	@echo "==> Install dependencies."
	#cd /debbuild/$(NAME) && find . -iname control 
	if [ -f "$(DOCKER_VOLUME)/GPG-KEYS-REPOS" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEYS-REPOS; fi
	cd /debbuild/$(NAME) && ./packbuild.py -r am -v $(AM_VERSION) -c $(AM_BRANCH) $(PACKBUILD_PARMS) 
	#cd /debbuild/$(NAME) && ./packbuild.py -r ss -v $(AM_VERSION) -c $(AM_BRANCH) -b $(RELEASE) -k$(GPG_ID)
	@echo "==> Build package."
	#cd /debbuild/$(NAME) && dpkg-buildpackage -us -uc -k
	@echo "==> Copying RPM files."
	mkdir -p $(DOCKER_VOLUME)/build/
	cp -rf /tmp/ampackbuilder/* $(DOCKER_VOLUME)/build/
	cd $(DOCKER_VOLUME)/build/ && dpkg-scanpackages . | gzip > Packages.gz

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
