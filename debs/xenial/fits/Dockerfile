FROM ubuntu:xenial

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE


RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs quilt


RUN mkdir -p /debbuild/ && cd /debbuild && \
	wget "https://launchpad.net/~archivematica/+archive/ubuntu/1.4/+files/fits_0.8.4-1~14.04.tar.gz" && \
	mkdir fits && \
	tar zxvf fits_0.8.4-1~14.04.tar.gz -C fits --strip-components=1

ADD debian /debbuild/$PACKAGE/debian

ENV JAVA_TOOL_OPTIONS -Dfile.encoding=UTF8
