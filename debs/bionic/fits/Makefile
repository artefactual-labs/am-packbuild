NAME          = fits
VERSION       ?= 1.1.0
RELEASE	      ?= 4~18.04
GIT_URL	      = https://github.com/harvard-lts/fits
GPG_ID        ?= 5236CA08
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"

.PHONY: build-docker-image build deb-build deb-clean deb-test update-changelog

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" --build-arg GIT_URL="$(GIT_URL)" --build-arg GIT_BRANCH="$(VERSION)" --build-arg PACKAGE="$(NAME)" .

update-changelog:
	@echo "==> Update changelog."
	@dch -v $(VERSION)-$(RELEASE) -D xenial "New upstream release"

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
	@echo "==> Apply patches."
	cd /debbuild/$(NAME) && QUILT_PATCHES=debian/patches/ quilt push -a 
	@echo "==> Install dependencies."
	cd /debbuild/$(NAME) && yes | mk-build-deps --install debian/control
	@echo "==> Update changelog."
	cd /debbuild/$(NAME) && dch -v $(VERSION)-$(RELEASE) -D xenial "New upstream release"
	@echo "==> Build package."
	cd /debbuild/$(NAME) && dpkg-buildpackage -k$(GPG_ID)
	@echo "==> Copying built  files."
	mkdir -p $(DOCKER_VOLUME)/build/
	cp  $(DEB_TOPDIR)/*.*  $(DOCKER_VOLUME)/build/ 

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/

# TODO: Create repo and test it
deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
