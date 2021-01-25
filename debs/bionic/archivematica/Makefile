NAME          = am-packbuild
PACKAGE	      ?= archivematica
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID ?= 0F4A4D31
PACKBUILD_EXTRA_ARGS ?=
#PACKBUILD_EXTRA_ARGS ?= "-b 1"
BRANCH     ?= qa/1.x
VERSION     ?= 1.8.1
RELEASE       ?= -1
BUILD_TYPE         ?= am
GIT_REPO ?= "https://github.com/artefactual"
GIT_HOSTNAME :=$(shell echo $(GIT_REPO) | sed -e 's/https:\/\///g' -e 's/git@//g'  -e 's/\:/\//g' | cut -d\/ -f1)
SSH_SOCKET  ?= $(SSH_AUTH_SOCK)


.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image build

build-docker-image: update-changelog
	@echo "==> Building Docker image with build environment."
	@docker build --rm --tag "$(DOCKER_IMAGE)" .

build:
	@echo "==> Building deb."
	@docker run \
                -v $(SSH_SOCKET):"/ssh-agent" \
                -e SSH_AUTH_SOCK="/ssh-agent" \
                -e BRANCH=$(BRANCH) \
		-e VERSION=$(VERSION) \
		-e RELEASE=$(RELEASE) \
                -e BUILD_TYPE=$(BUILD_TYPE) \
                -e GPG_ID=$(GPG_ID) \
		-e GPG_KEY \
		-e GIT_REPO="$(GIT_REPO)" \
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
	@if [ x"$$GPG_KEY" != x ]; then echo "$$GPG_KEY" | gpg --import - ; fi
	#@cd /debbuild/$(NAME) && ./packbuild.py -r $(BUILD_TYPE) -v $(VERSION) -c $(BRANCH) -k$(GPG_ID) $(PACKBUILD_EXTRA_ARGS)
	@cd /debbuild/$(NAME)
	@echo "==> Clone code."
	mkdir -p ~/.ssh/
	ssh-keyscan -t rsa $(GIT_HOSTNAME) >> ~/.ssh/known_hosts || true
	mkdir -p src/$(PACKAGE)
	rm -rf src/
	@git clone \
		--quiet \
		--branch $(BRANCH) \
		--depth 1 \
		--single-branch \
			$(GIT_REPO)/$(PACKAGE) src/$(PACKAGE)
	./build.sh
	mkdir -p repo/
	cp -rf src/archivematica/src/archivematica-* repo
	cd  repo && dpkg-scanpackages . | gzip > Packages.gz

deb-clean:
	@echo "==> Cleaning up previous builds."
	@rm -rf $(DOCKER_VOLUME)/repo/
	@rm -rf $(DOCKER_VOLUME)/src/

cleanup:
	@echo "==> Remove artifacts created as root. "
	@docker run -i \
		--rm \
		--volume "$(shell cd ../../ && pwd):$(DEB_TOPDIR)/$(NAME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
		rm -rf /src/repo/ /src/src/

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
