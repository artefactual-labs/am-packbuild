NAME          = bulk_extractor
VERSION       ?= 2.1.1
RELEASE	      ?= 1~22.04
GIT_URL	      = https://github.com/simsong/bulk_extractor
GIT_BRANCH    = 2.1.1
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

update-changelog: build-docker-image
	@echo "==> Update changelog inside Docker."
	@docker run --rm \
		--user $(shell id -u):$(shell id -g) \
		--workdir "$(DOCKER_VOLUME)" \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
		dch -v $(VERSION)-$(RELEASE) -D $(DISTRO_CODENAME) "New upstream release"

build:
	@echo "==> Building deb."
	@docker run --rm \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) deb-build

deb-build: deb-clean
	echo "==> Install dependencies."; \
	cd /debbuild/$(NAME) && yes | mk-build-deps --install debian/control; \
	echo "==> Update changelog."; \
	cd /debbuild/$(NAME) && dch -v $(VERSION)-$(RELEASE) -D $(DISTRO_CODENAME) "New upstream release"; \
	echo "==> Build package (unsigned)."; \
	cd /debbuild/$(NAME) && dpkg-buildpackage -us -uc; \
	echo "==> Copying built  files."; \
	mkdir -p $(DOCKER_VOLUME)/build/; \
	cp  $(DEB_TOPDIR)/*.*  $(DOCKER_VOLUME)/build/

deb-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(DOCKER_VOLUME)/build/

deb-test:
	@DEB_FILE="$(firstword $(wildcard build/$(NAME)_$(VERSION)-$(RELEASE)_*.deb) $(wildcard build/$(subst _,-,$(NAME))_$(VERSION)-$(RELEASE)_*.deb))"; \
	if [ -z "$$DEB_FILE" ]; then \
		echo "No built package found under build/. Run 'make build' first."; \
		exit 1; \
	fi; \
	docker run --rm \
		--volume="$(shell pwd):$(DOCKER_VOLUME)" \
		ubuntu:$(DISTRO_CODENAME) \
		bash -c "set -euo pipefail; \
			echo '==> Updating apt cache.'; \
			apt-get update >/dev/null; \
			echo '==> Installing bulk_extractor package.'; \
			apt-get install -y --no-install-recommends \"$(DOCKER_VOLUME)/$$DEB_FILE\" >/dev/null; \
			echo '==> Verifying bulk_extractor runs.'; \
			OUT_DIR=\$$(mktemp -d); \
			bulk_extractor --version >/dev/null; \
			bulk_extractor -o \"\$$OUT_DIR\" /usr/share/pixmaps/debian-logo.png; \
			rm -rf \"\$$OUT_DIR\""
