all: build

build:
	make -C ./siegfried
	make -C ./storage-service
	make -C ./storage-service-frontend

clean:
	find . -name "*.rpm" -delete
