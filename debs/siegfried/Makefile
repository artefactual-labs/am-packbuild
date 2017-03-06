NAME          = siegfried
VERSION       = 1.6.7
RELEASE	      = 2
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

deb-build: deb-clean
	@echo "==> Install dependencies."
	cd /debbuild/siegfried && yes | mk-build-deps --install debian/control
	@echo "==> Build package."
	cd /debbuild/siegfried && GOPATH=/usr/lib/go-1.6/bin dpkg-buildpackage -k5236CA08 
	@echo "==> Copying RPM files."
	cp -p $(DEB_TOPDIR)/*.* $(DOCKER_VOLUME)
	#hip -p $(DEB_TOPDIR)/SRPMS/$(NAME)-*.src.rpm $(DOCKER_VOLUME)

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	#@rm -rf $(DEB_TOPDIR)

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:trusty echo "Create repo and install package"
