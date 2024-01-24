FROM ubuntu:jammy

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE
ARG DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs quilt maven git openjdk-8-jdk-headless



RUN mkdir -p /debbuild/ && cd /debbuild && \
	git clone $GIT_URL && \
	cd $PACKAGE && \
	git checkout $GIT_BRANCH

#ADD debian /debbuild/$PACKAGE/debian
