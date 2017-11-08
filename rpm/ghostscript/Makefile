NAME          = ghostscript
VERSION       = 9.20
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "_etcdir $(DOCKER_VOLUME)/etc" \
	--define "name $(NAME)" \
	--define "version $(VERSION)"

.PHONY: build-docker-image build rpm-build rpm-clean rpm-test

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "$(DOCKER_IMAGE)" .

build:
	@echo "==> Building RPM."
	@docker run --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) rpm-build

rpm-build: rpm-clean
	@echo "==> Preparing environment for rpmbuild."
	mkdir -p $(RPM_TOPDIR)/SOURCES
	yum-builddep -y ghostscript
	yum install -y openjpeg2-devel
	wget "https://kojipkgs.fedoraproject.org//packages/ghostscript/9.20/12.fc27/src/ghostscript-9.20-12.fc27.src.rpm" -O ghostscript-9.20-12.fc27.src.rpm
	rpmbuild $(RPMBUILD_ARGS) --rebuild ghostscript-9.20-12.fc27.src.rpm

	@echo "==> Copying RPM files."
	cp -prf $(RPM_TOPDIR)/RPMS/* $(DOCKER_VOLUME)

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)

rpm-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" centos:7 bash -c "yum install -y epel-release && yum localinstall -y --nogpgcheck $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm"
