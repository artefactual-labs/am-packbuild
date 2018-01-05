FROM ubuntu:xenial


RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs quilt


RUN mkdir -p /debbuild/ && cd /debbuild && \
    apt-get build-dep -y hashdeep
