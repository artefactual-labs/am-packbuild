FROM ubuntu:bionic

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE


RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs quilt


RUN mkdir -p /debbuild/ && cd /debbuild && \
	git clone $GIT_URL && \
	cd $PACKAGE && \
	git checkout $GIT_BRANCH

ADD debian /debbuild/$PACKAGE/debian

ENV JAVA_TOOL_OPTIONS -Dfile.encoding=UTF8
