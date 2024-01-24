FROM ubuntu:bionic

ARG SRC_URL
ARG PACKAGE
ARG SRC_VERSION
ARG SRC_SHA256

RUN apt-get update

RUN apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs

RUN mkdir -p /debbuild/ && cd /debbuild && \
	wget $SRC_URL && \
	echo "$SRC_SHA256  $PACKAGE-$SRC_VERSION.tar.gz" | sha256sum --check && \
	tar xfz $PACKAGE-$SRC_VERSION.tar.gz && \
        mv $PACKAGE-$SRC_VERSION $PACKAGE && \
	cd $PACKAGE

ADD debian /debbuild/$PACKAGE/debian
