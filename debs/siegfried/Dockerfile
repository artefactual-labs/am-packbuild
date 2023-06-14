FROM ubuntu:xenial

# Environmnet variables needed during build
ENV GOVERSION 1.19
ENV GOOS linux
ENV GOARCH amd64
ARG DEBIAN_FRONTEND=noninteractive

# Environment variables needed during runtime
ENV GOPATH /go
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin:/go/bin

RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper curl \
    devscripts equivs dh-golang && \
    curl -sO https://storage.googleapis.com/golang/go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz && \
    tar -C /usr/local -xzf go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz && \
    rm go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz

# Install build dependencies

ENV DEBFULLNAME "Artefactual Systems"
ENV DEBEMAIL "sysadmin@artefactual.com"
