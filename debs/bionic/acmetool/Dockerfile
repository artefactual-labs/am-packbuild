FROM ubuntu:bionic

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential debhelper devscripts \
    dpkg-dev equivs git golang-go libcap-dev make quilt

RUN mkdir -p /debbuild/ && cd /debbuild && \
        git config --global http.followRedirects true &&\
        git clone $GIT_URL && \
        cd $PACKAGE && \
        git checkout $GIT_BRANCH

ADD debian /debbuild/$PACKAGE/debian
