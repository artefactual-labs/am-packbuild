FROM ubuntu:xenial

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE

RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs dh-golang golang-go

# dh-golang doesn't support parameters, and we need to run it with -tags archivematica
ADD files/golang.pm /usr/share/perl5/Debian/Debhelper/Buildsystem/golang.pm


RUN mkdir -p /debbuild/ && cd /debbuild && \
	git clone $GIT_URL && \
	cd siegfried && \
	git checkout v1.6.7

ADD debian /debbuild/siegfried/debian

ADD GPG-KEYS-REPOS /root/key.gpg
RUN gpg --import /root/key.gpg

# Install build dependencies
ENV GOPATH /usr/share/go-1.6/
RUN go get -u -v golang.org/x/tools/go/loader
