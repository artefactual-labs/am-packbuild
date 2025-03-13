NAME          = nginx-mod-geoip2
VERSION       ?= 1.20.1
RPM_TOPDIR    = "/rpmbuild"
DOCKER_VOLUME = "/src"
DOCKER_IMAGE  = "rpmbuild-$(NAME)-$(VERSION)"
NGINX_GEOIP2_VERSION = 3.4
NGINX_GEOIP2_SRC_TARBALL = "https://github.com/leev/ngx_http_geoip2_module/archive/refs/tags/${NGINX_GEOIP2_VERSION}.tar.gz"

RPMBUILD_ARGS := \
	--define "_topdir $(RPM_TOPDIR)" \
	--define "_etcdir $(DOCKER_VOLUME)/etc" \
	--define "name $(NAME)" \
	--define "version $(VERSION)" \
	--define "nginx_geoip2_version $(NGINX_GEOIP2_VERSION)"

.PHONY: build-docker-image build rpm-build rpm-clean rpm-test

all: build-docker-image build

build-docker-image:
	@echo "==> Building Docker image with build environment and pass VERSION as build argument."
	@docker build --tag "${DOCKER_IMAGE}" --build-arg VERSION=$(VERSION) .

build:
	@echo "==> Building RPM inside Docker container."
	@docker run --rm --volume "$(shell pwd):$(DOCKER_VOLUME)" $(DOCKER_IMAGE) make -C $(DOCKER_VOLUME) rpm-build

rpm-build: rpm-clean
	@echo "==> Downloading sources."
	mkdir -p $(RPM_TOPDIR)
	cp $(DOCKER_VOLUME)/package.spec $(RPM_TOPDIR)/package.spec
	mkdir -p $(RPM_TOPDIR)/SOURCES/files
	wget -O $(RPM_TOPDIR)/SOURCES/$(NGINX_GEOIP2_VERSION).tar.gz ${NGINX_GEOIP2_SRC_TARBALL}

	@echo "==> Running rpmbuild."
	rpmbuild $(RPMBUILD_ARGS) -ba --clean $(RPM_TOPDIR)/package.spec

	@echo "==> Copying RPM files."
	cp -p $(RPM_TOPDIR)/RPMS/x86_64/$(NAME)-$(VERSION)*.x86_64.rpm $(DOCKER_VOLUME)/
	cp -p $(RPM_TOPDIR)/SRPMS/$(NAME)-$(VERSION)*.src.rpm $(DOCKER_VOLUME)/

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)

cleanup:
	@echo "==> Remove artifacts created as root."
	@docker run -i  \
		--rm \
		--volume "$(shell pwd):$(DOCKER_VOLUME)" \
		$(DOCKER_IMAGE) \
		bash -c "rm -rf /src/*.rpm"

rpm-test:
	docker run --rm --volume="$(shell pwd):$(DOCKER_VOLUME)" rockylinux:9 bash -c "rpm -i $(DOCKER_VOLUME)/$(NAME)-$(VERSION)*.rpm && sf -version"
