FROM ubuntu:xenial

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE


RUN apt-get update

RUN apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs


RUN mkdir -p /debbuild/ && cd /debbuild && \
	git clone $GIT_URL && \
	cd $PACKAGE && \
	git checkout $GIT_BRANCH

ADD debian /debbuild/$PACKAGE/debian

