NAME          = atool
VERSION       = 0.39.0
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
	cp $(DOCKER_VOLUME)/package.spec $(RPM_TOPDIR)/package.spec
	wget -O $(RPM_TOPDIR)/SOURCES/atool-$(VERSION).tar.gz http://download-mirror.savannah.gnu.org/releases/atool/atool-$(VERSION).tar.gz
	wget -O $(RPM_TOPDIR)/SOURCES/atool-$(VERSION).tar.gz.sig http://download-mirror.savannah.gnu.org/releases/atool/atool-$(VERSION).tar.gz.sig
	cp files/* $(RPM_TOPDIR)/SOURCES/
	yum-builddep -y $(RPM_TOPDIR)/package.spec
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec

	@echo "==> Copying RPM files."
	cp -p $(RPM_TOPDIR)/RPMS/noarch/$(NAME)-*.noarch.rpm $(DOCKER_VOLUME)
	cp -p $(RPM_TOPDIR)/SRPMS/$(NAME)-*.src.rpm $(DOCKER_VOLUME)

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)

rpm-test:
	@docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" centos:7 bash -c "yum install -y epel-release && yum localinstall -y --nogpgcheck $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm"
