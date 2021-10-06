DEB_REPOSITORY = "$(shell pwd)/_deb_repository"

all: build createrepo

build:
	#make -C ./siegfried
	make -C ./bionic/archivematica-storage-service
	make -C ./bionic/archivematica
	#make -C ./nailgun
	#make -C ./bionic/fits
	#make -C ./atool
	#make -C ./bionic/jhove

createrepo: cleanrepo
	mkdir -p $(DEB_REPOSITORY) || true
	find ./bionic/archivematica-storage-service ./bionic/archivematica -name "*.deb" | grep -v src | xargs -IF cp -f F $(DEB_REPOSITORY)
	docker run --rm --volume "$(DEB_REPOSITORY):/deb-repository" ubuntu:18.04 bash -c "apt-get update && apt-get install -y dpkg-dev && cd /deb-repository && dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz"

clean: cleanrepo
	find . -name "*.deb" -delete

cleanrepo:
	rm -rf $(DEB_REPOSITORY)
