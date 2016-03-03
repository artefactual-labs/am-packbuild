NAME         = archivematica-storage-service
VERSION      = 0.7.1dev
DOCKER_IMAGE = "rpmbuild-$(NAME)-$(VERSION)"


.PHONY: build-docker-image build rpm-build rpm-clean test-version

all: build-docker-image build

clean: rpm-clean docker-clean

build-docker-image:
	@echo "==> Building Docker image with build environment."
	@docker build --tag "${DOCKER_IMAGE}" .

build:
	@echo "==> Building RPM."
	@docker run --volume "$(shell pwd):/rpm" ${DOCKER_IMAGE} rpmvenv --core_version=${VERSION} --destination /rpm --verbose  /src/archivematica-storage-service/config.json

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(shell pwd)/${NAME}-${VERSION}*.rpm

docker-clean:
	@docker rmi "${DOCKER_IMAGE}" 

test-version:
	@docker run --volume="$(shell pwd):/rpm" centos:7 bash -c "rpm -ivh /rpm/$(NAME)-$(VERSION)*.rpm"
