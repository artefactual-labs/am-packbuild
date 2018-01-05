NAME          = hashdeep
VERSION       ?= 4.4
RELEASE       ?= 1~16.04
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"

.PHONY: build-docker-image build deb-build deb-clean

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" .

build:
	@echo "==> Building deb."
	docker run --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build: deb-clean
	@echo "==> Install repository."
	echo 'deb-src http://archive.ubuntu.com/ubuntu/ artful universe' >> /etc/apt/sources.list && apt-get update
	@echo "==> Download source package"
	cd /debbuild/ && apt-get source hashdeep
	@echo "==> Rebuild package."
	cd /debbuild/$(NAME)-$(VERSION) && sed -i 's/>=10/>=9/g' debian/control
	@echo "==> Build package."
	cd /debbuild/$(NAME)-$(VERSION) && dpkg-buildpackage 
	@echo "==> Copying built  files."
	mkdir -p $(DOCKER_VOLUME)/build/
	cp  $(DEB_TOPDIR)/$(NAME)_*.* $(DOCKER_VOLUME)/build/ 

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/
