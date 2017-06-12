FROM ubuntu:xenial

ARG GIT_URL
ARG GIT_BRANCH
ARG PACKAGE


RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs



RUN wget -O /tmp/pip.py https://bootstrap.pypa.io/get-pip.py && python /tmp/pip.py

RUN apt-get install -y libffi-dev libssl-dev libxslt-dev dh-virtualenv python-dev

