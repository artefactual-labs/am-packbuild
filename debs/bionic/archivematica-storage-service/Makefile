NAME          = am-packbuild
PACKAGE       = archivematica-storage-service
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(PACKAGE)-$(VERSION)"
GPG_ID        ?= 0F4A4D31
BRANCH        ?= qa/0.x
VERSION       ?= 0.19.0
RELEASE       ?= -1
GIT_REPO      = "https://github.com/artefactual/archivematica-storage-service"

.DEFAULT_GOAL := build

.PHONY: build-docker-image
build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --rm --tag "$(DOCKER_IMAGE)" .

.PHONY: build
build: build-docker-image
	@echo "==> Building deb."
	@docker run \
		-e BRANCH=$(BRANCH) \
		-e VERSION=$(VERSION) \
		-e RELEASE=$(RELEASE) \
		-e PACKAGE=$(PACKAGE) \
		-e GPG_ID=$(GPG_ID) \
		-e GPG_KEY \
		-e GIT_REPO="$(GIT_REPO)" \
		--rm \
		--volume "$(shell cd ../../ && pwd):$(DEB_TOPDIR)/$(NAME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
			make -C $(DOCKER_VOLUME) deb-build

.PHONY: deb-build
deb-build: deb-clean git-clone import-gpg-key
	@cd /debbuild/$(NAME)
	./build.sh
	mkdir -p repo/
	cp -rf src/archivematica-*.* repo
	cd repo && dpkg-scanpackages . | gzip > Packages.gz

.PHONY: import-gpg-key
import-gpg-key:
	@if [ -f "$(DOCKER_VOLUME)/GPG-KEY" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEY; fi
	@if [ x"$$GPG_KEY" != x ]; then echo "$$GPG_KEY" | gpg --import - ; fi

.PHONY: git-clone
git-clone:
	@git clone \
		--quiet \
		--branch $(BRANCH) \
		--depth 1 \
		--single-branch \
			$(GIT_REPO) src/$(PACKAGE)

.PHONY: deb-clean
deb-clean:
	@echo "==> Cleaning up previous builds."
	@rm -rf $(DOCKER_VOLUME)/repo/
	@rm -rf $(DOCKER_VOLUME)/src/

.PHONY: cleanup
cleanup: build-docker-image
	@echo "==> Remove artifacts created as root."
	@docker run -i \
		--rm \
		--volume "$(shell cd ../../ && pwd):$(DEB_TOPDIR)/$(NAME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
		rm -rf /src/repo/ /src/src/
