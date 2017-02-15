NAME          = siegfried
VERSION       = 1.6.7
RELEASE	      = 1
GIT_URL	      = https://github.com/richardlehane/siegfried/
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"

.PHONY: build-docker-image build deb-build deb-clean deb-test

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" --build-arg GIT_URL="$(GIT_URL)" --build-arg GIT_BRANCH=v"$(VERSION)" --build-arg PACKAGE="$(NAME)" .

build:
	@echo "==> Building deb."
	@docker run --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

update-changelog:
	@echo "==> Update changelog."
	@dch -v $(VERSION)-$(RELEASE) -D trusty "New upstream release"


deb-build: deb-clean
	@echo "==> Install dependencies."
	cd /debbuild/siegfried && yes | mk-build-deps --install debian/control
	@echo "==> Build package."
	cd /debbuild/siegfried && GOPATH=/usr/lib/go-1.6/bin dpkg-buildpackage -us -uc
	@echo "==> Copying built files."
	mkdir -p $(DOCKER_VOLUME)/build/
	cp -p $(DEB_TOPDIR)/*.* $(DOCKER_VOLUME)/build/

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DEB_TOPDIR)/build

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
