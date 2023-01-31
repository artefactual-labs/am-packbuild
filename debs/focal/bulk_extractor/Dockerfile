FROM ubuntu:focal

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs automake autotools-dev

RUN mkdir -p /debbuild/ && cd /debbuild && \
	git clone --recursive $GIT_URL && \
	cd $PACKAGE && \
	git checkout $GIT_BRANCH && \
        sh bootstrap.sh

ADD debian /debbuild/$PACKAGE/debian

