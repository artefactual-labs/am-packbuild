FROM ubuntu:trusty

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE


RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs


RUN mkdir -p /debbuild/ && cd /debbuild && \
	git clone $GIT_URL && \
	cd $PACKAGE && \
	git checkout $GIT_BRANCH

ADD GPG-KEYS-REPOS /root/key.gpg
RUN gpg --import /root/key.gpg

RUN apt-get install -y libffi-dev libssl-dev libxslt-dev

