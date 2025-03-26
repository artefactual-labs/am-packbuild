NAME          = enduro
PACKAGE       = enduro
VERSION       ?= 0.11.0
RELEASE       ?= 1
BRANCH        ?= v0.11.0
GIT_URL       = https://github.com/artefactual-sdps/enduro/
DEB_TOPDIR    = "/debbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "debbuild-$(NAME)-$(VERSION)"
GPG_ID        ?= 0F4A4D31
DISTRO_CODENAME = noble
.PHONY: build-docker-image build deb-build deb-clean deb-test

all: build-docker-image get-code build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --rm --tag "$(DOCKER_IMAGE)"  .

build:
	@echo "==> Building deb."
	@docker run --rm \
			-e BRANCH=$(BRANCH) \
			-e GIT_URL=$(GIT_URL) \
				-e VERSION=$(VERSION) \
				-e RELEASE=$(RELEASE) \
				-e BUILD_TYPE=$(BUILD_TYPE) \
				-e GPG_ID=$(GPG_ID) \
				-e GPG_KEY \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build:
	# Update debian/folder and changelog, and install dependencies
	@echo "==> Build package."
	git config --global --add safe.directory /src/src/enduro
	cd src/$(PACKAGE) && PATH=${PATH} GOPATH=${GOPATH} && ./hack/build_dist.sh -o enduro ./cmd/enduro
	cd src/$(PACKAGE) && PATH=${PATH} GOPATH=${GOPATH} && ./hack/build_dist.sh -o enduro-am-worker ./cmd/enduro-am-worker
	cd src/ && rm -f *.deb 
	cd src/ && cp /src/.fpm . 
	cd src/ && PATH=${PATH} fpm --name enduro --version ${VERSION} -p enduro_${VERSION}-${RELEASE}_amd64.deb  enduro=/usr/bin/enduro enduro.toml=/etc/enduro.toml
	cd src/ && PATH=${PATH} fpm --name enduro-am-worker --version ${VERSION} --description "enduro worker package" -p enduro-am-worker_${VERSION}-${RELEASE}_amd64.deb  enduro-am-worker=/usr/bin/enduro-am-worker
	@echo "==> Copying DEB files."
	mkdir -p build
	cp src/$(PACKAGE)*.deb build/

get-code:
	@echo "==> Get code."
	@mkdir -p src/
	@docker run --rm \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) rm -rf $(DOCKER_VOLUME)/src/$(PACKAGE)
	@git clone \
			--quiet \
			--branch ${BRANCH} \
			--recurse-submodules $(GIT_URL) \
		src/$(PACKAGE)

deb-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" ubuntu:$(DISTRO_CODENAME) echo "Create repo and install package"
