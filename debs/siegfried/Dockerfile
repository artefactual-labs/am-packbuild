FROM ubuntu:xenial

# Environmnet variables needed during build
ENV GOVERSION 1.11
ENV GOOS linux
ENV GOARCH amd64

# Environment variables needed during runtime
ENV GOPATH /go
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin:/go/bin

RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper curl \
    devscripts equivs dh-golang && \
    curl -sO https://storage.googleapis.com/golang/go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz && \
    tar -C /usr/local -xzf go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz && \
    rm go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz

# dh-golang doesn't support parameters, and we need to run it with -tags archivematica
ADD files/golang.pm /usr/share/perl5/Debian/Debhelper/Buildsystem/golang.pm

# Install build dependencies

ENV DEBFULLNAME "Artefactual Systems"
ENV DEBEMAIL "sysadmin@artefactual.com"
