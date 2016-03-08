NAME         = archivematica-storage-service
VERSION      = 0.6.1
URL          = "https://github.com/richardlehane/siegfried/archive/v$(VERSION).tar.gz"
RPM_TOPDIR   = "/rpmbuild"
DOCKER_IMAGE = "rpmbuild-$(NAME)-$(VERSION)"

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
	@echo "==> Building RPM."
	@docker run --rm --volume "$(shell pwd):/src" ${DOCKER_IMAGE} make -C /src rpm-build

rpm-build: rpm-clean
	mkdir -p $(RPM_TOPDIR)
	cp /src/package.spec $(RPM_TOPDIR)/package.spec
	yum-builddep -y $(RPM_TOPDIR)/package.spec
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec
	cp -p $(RPM_TOPDIR)/RPMS/x86_64/$(NAME)-$(VERSION)*.x86_64.rpm /src/

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)


rpm-test:
	@docker run --rm --volume="$(shell pwd):/src" centos:7 bash -c "yum install -y epel-release && yum localinstall -y --nogpgcheck /src/$(NAME)-$(VERSION)*.rpm"
