DEB_REPOSITORY = "$(shell pwd)/_deb_repository"

all: build createrepo

build:
	make -C ./archivematica-storage-service
	make -C ./archivematica

createrepo: cleanrepo
	mkdir -p $(DEB_REPOSITORY) || true
	find ./archivematica-storage-service ./archivematica -name "*.deb" | grep -v src | xargs -IF cp -f F $(DEB_REPOSITORY)
	docker run --rm --volume "$(DEB_REPOSITORY):/deb-repository" ubuntu:22.04 bash -c "apt-get update && apt-get install -y dpkg-dev && cd /deb-repository && dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz"

clean: cleanrepo
	find . -name "*.deb" -delete

cleanrepo:
	rm -rf $(DEB_REPOSITORY)
