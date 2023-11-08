YUM_REPOSITORY = "$(shell pwd)/_yum_repository"

all: build createrepo

build:
	make -C ./archivematica
	make -C ./archivematica-storage-service
	make -C ./siegfried
	make -C ./nailgun
	make -C ./fits
	make -C ./jhove
	make -C ./cadence
	make -C ./cadence-web
	make -C ./enduro
	make -C ./temporal
	make -C ./temporal-ui
	make -C ./tctl

createrepo: cleanrepo
	mkdir -p $(YUM_REPOSITORY) || true
	find . -name "*.rpm" | xargs -IF cp -f F $(YUM_REPOSITORY)
	docker run --rm --volume "$(YUM_REPOSITORY):/yum-repository" rockylinux:9 bash -c "yum install -y createrepo && createrepo /yum-repository"

clean: cleanrepo
	find . -name "*.rpm" -delete

cleanrepo:
	rm -rf $(YUM_REPOSITORY)
