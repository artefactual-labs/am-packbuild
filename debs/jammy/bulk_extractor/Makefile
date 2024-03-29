NAME          = bulk_extractor
VERSION       ?= 2.0.0
RELEASE	      ?= 1~22.04
GIT_URL	      = https://github.com/simsong/bulk_extractor
GIT_BRANCH    = 2.0.0
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID        ?= 5236CA08
DISTRO_CODENAME = jammy

.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" --build-arg GIT_URL="$(GIT_URL)" --build-arg GIT_BRANCH=v"$(GIT_BRANCH)" --build-arg PACKAGE="$(NAME)" .

update-changelog:
	@echo "==> Update changelog."
	@dch -v $(VERSION)-$(RELEASE) -D $(DISTRO_CODENAME) "New upstream release"

build:
	@echo "==> Building deb."
	@docker run --rm \
		-e GPG_ID=$(GPG_ID) \
		-e GPG_KEY \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build: deb-clean
	@echo "===> Install gpg key"
	if [ -f "$(DOCKER_VOLUME)/GPG-KEY" ]; then gpg --import $(DOCKER_VOLUME)/GPG-KEY; fi
	if [ x"$$GPG_KEY" != x ]; then echo "$$GPG_KEY" | gpg --import - ; fi
	@echo "==> Install dependencies."
	cd /debbuild/$(NAME) && yes | mk-build-deps --install debian/control
	@echo "==> Update changelog."
	cd /debbuild/$(NAME) && dch -v $(VERSION)-$(RELEASE) -D $(DISTRO_CODENAME) "New upstream release"

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
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:$(DISTRO_CODENAME) echo "Create repo and install package"
