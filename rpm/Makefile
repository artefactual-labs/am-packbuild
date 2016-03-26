YUM_REPOSITORY = "$(shell pwd)/_yum_repository"

all: build createrepo

build:
	make -C ./siegfried
	make -C ./storage-service
	make -C ./archivematica
	make -C ./nailgun
	make -C ./fits
	make -C ./bagit
	make -C ./atool
	make -C ./jhove

createrepo: cleanrepo
	mkdir -p $(YUM_REPOSITORY) || true
	find . -name "*.rpm" | xargs -IF cp -f F $(YUM_REPOSITORY)
	docker run --rm --volume "$(YUM_REPOSITORY):/yum-repository" centos:7 bash -c "yum install -y createrepo && createrepo /yum-repository"

clean: cleanrepo
	find . -name "*.rpm" -delete

cleanrepo:
	rm -rf $(YUM_REPOSITORY)
