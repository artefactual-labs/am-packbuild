NAME          = dh-virtualenv
COMMIT       ?= b7101f62fa78
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(COMMIT)"

.PHONY: build-docker-image build deb-build deb-clean

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" .

build:
	@echo "==> Building deb."
	docker run \
               -e COMMIT=$(COMMIT) \
               --rm \
               --volume "$(shell pwd):$(DOCKER_VOLUME)" \
               $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build: deb-clean
	@echo "==> Download source package"
	cd /debbuild/ && \
	git clone https://github.com/spotify/dh-virtualenv.git
	cd /debbuild/$(NAME) && git checkout $(COMMIT)
	@echo "==> Install build dependencies."
	cd /debbuild/$(NAME) && yes | mk-build-deps -ri
	@echo "==> Build package."
	cd /debbuild/$(NAME) && dpkg-buildpackage -us -uc -b
	@echo "==> Copying built files."
	mkdir -p $(DOCKER_VOLUME)/build/
	cp  $(DEB_TOPDIR)/$(NAME)_*.* $(DOCKER_VOLUME)/build/ 

deb-clean:
	@echo "==> Cleaning up previous builds."
	@rm -rf $(DOCKER_VOLUME)/build/
