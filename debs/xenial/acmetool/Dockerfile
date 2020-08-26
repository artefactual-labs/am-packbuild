FROM ubuntu:xenial

# Environmnet variables needed during build
ENV GOVERSION 1.15
ENV GOOS linux
ENV GOARCH amd64

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE

# Environment variables needed during runtime
ENV GOPATH /go
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin:/go/bin

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential curl debhelper devscripts \
    dpkg-dev equivs git libcap-dev make quilt

RUN mkdir -p /debbuild/ && cd /debbuild && \
        git config --global http.followRedirects true &&\
        git clone $GIT_URL && \
        cd $PACKAGE && \
        git checkout $GIT_BRANCH

RUN curl -sO https://storage.googleapis.com/golang/go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz && \
    tar -C /usr/local -xzf go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz && \
    rm go${GOVERSION}.${GOOS}-${GOARCH}.tar.gz


ADD debian /debbuild/$PACKAGE/debian
