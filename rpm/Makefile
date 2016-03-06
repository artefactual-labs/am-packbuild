NAME         = siegfried
VERSION      = 1.4.5
URL          = "https://github.com/richardlehane/siegfried/archive/v$(VERSION).tar.gz"
RPM_TOPDIR   = "/root/rpmbuild"
DOCKER_IMAGE = "rpmbuild-$(NAME)-$(VERSION)"


.PHONY: rpm-clean common storage-service

all: rpm-clean common storage-service mcp-server mcp-client dashboard

storage-service:
	@echo "==> archivematica-storage-service rpm."
	@yum-builddep archivematica-storage-service/archivematica-storage-service.spec
	@rpmbuild -ba --clean archivematica-storage-service/archivematica-storage-service.spec
	@cp /root/rpmbuild/RPMS/x86_64/archivematica-storage-service*.rpm . 


common:
	@echo "==> archivematica-common rpm."
	@yum-builddep archivematica-common/archivematica-common.spec
	@rpmbuild -ba --clean archivematica-common/archivematica-common.spec
	@cp /root/rpmbuild/RPMS/x86_64/archivematica-common*.rpm . 
	
mcp-server:
	@echo "==> archivematica-mcp-server rpm."
	@yum-builddep archivematica-mcp-server/archivematica-mcp-server.spec
	@rpmbuild -ba --clean archivematica-mcp-server/archivematica-mcp-server.spec
	@cp /root/rpmbuild/RPMS/x86_64/archivematica-mcp-server*.rpm . 


mcp-client:
	@echo "==> archivematica-mcp-client rpm."
	@yum-builddep archivematica-mcp-client/archivematica-mcp-client.spec
	@rpmbuild -ba --clean archivematica-mcp-client/archivematica-mcp-client.spec
	@cp /root/rpmbuild/RPMS/x86_64/archivematica-mcp-client*.rpm . 
	
dashboard:
	@echo "==> archivematica-dashboard rpm."
	@yum-builddep archivematica-dashboard/archivematica-dashboard.spec
	@rpmbuild -ba --clean archivematica-dashboard/archivematica-dashboard.spec
	@cp /root/rpmbuild/RPMS/x86_64/archivematica-dashboard*.rpm . 

rpm-clean:
	@echo "==> Cleaning up previous RPMs builds."
	@rm -rf $(RPM_TOPDIR)
	@rm -rf *.rpm

test-version:
	@docker run --volume="$(shell pwd):/src" centos:7 bash -c "rpm -i /src/$(NAME)-$(VERSION)*.rpm && sf -version"
