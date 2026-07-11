FROM rockylinux:9

ARG GOVERSION=1.25.0
ARG GOOS=linux
ARG GOARCH=amd64

# Environment variables needed during runtime
ENV GOPATH=/go
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOVERSION=${GOVERSION}
ENV GOOS=${GOOS}
ENV GOARCH=${GOARCH}

RUN yum -y install rpm-build make git && \
	curl -sO https://dl.google.com/go/go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz && \
	tar -C /usr/local -xzf go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz && \
	rm go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz
