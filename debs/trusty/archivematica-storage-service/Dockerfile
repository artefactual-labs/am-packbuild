FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs quilt

RUN wget -O /tmp/pip.py https://bootstrap.pypa.io/get-pip.py && python /tmp/pip.py

# Dependencies are also obtained in the debian build script, this speeds up the process of building packages

