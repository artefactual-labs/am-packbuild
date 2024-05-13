NAME          = enduro
VERSION       = 0.1.0
RPM_TOPDIR    = "/rpmbuild"
BRANCH	     ?= dev/sfa
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"
ENDURO_SRC = "/src/enduro-sfa"

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "name $(NAME)" \
	--define "version $(VERSION)"

.PHONY: build-docker-image build rpm-build rpm-clean rpm-test

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "${DOCKER_IMAGE}" .

build:
	@echo "==> Building RPM inside Docker container."
	@docker run \
	       -e BRANCH="$(BRANCH)" \
		--rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) rpm-build

rpm-build: rpm-clean
	@echo "==> Downloading enduro code."
	mkdir -p $(ENDURO_SRC)
	git clone --branch $(BRANCH) --depth 1 https://github.com/artefactual-sdps/enduro.git $(ENDURO_SRC)

	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/{BUILD,RPMS,SRPMS}
	mkdir -p $(RPM_TOPDIR)/SOURCES/$(NAME)-$(VERSION)
	cp -rf -p $(DOCKER_VOLUME)/files/* $(ENDURO_SRC)/
	cp $(DOCKER_VOLUME)/package.spec $(ENDURO_SRC)/package.spec

	@echo "==> Running rpmbuild."
	cd $(ENDURO_SRC) && rpmbuild $(RPMBUILD_ARGS) -ba --clean package.spec


	@echo "==> Copying RPM files."
	cp -p $(RPM_TOPDIR)/RPMS/x86_64/$(NAME)*-$(VERSION)*.x86_64.rpm $(DOCKER_VOLUME)/
	cp -p $(RPM_TOPDIR)/SRPMS/$(NAME)*-$(VERSION)*.src.rpm $(DOCKER_VOLUME)/

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR) $(ENDURO_SRC)


rpm-test:
	docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" rockylinux:9 bash -c "rpm -i $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm && sf -version"

cleanup:
	@echo "==> Remove artifacts created as root."
	@docker run -i  \
		--rm \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
		bash -c "rm -rf /src/*.rpm /src/enduro-sfa"

