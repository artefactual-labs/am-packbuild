FROM ubuntu:xenial


RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs dh-golang software-properties-common python-software-properties 

RUN add-apt-repository ppa:gophers/archive
RUN apt-get update && apt-get install -y golang-1.7

# dh-golang doesn't support parameters, and we need to run it with -tags archivematica
ADD files/golang.pm /usr/share/perl5/Debian/Debhelper/Buildsystem/golang.pm


# Install build dependencies
ENV GOPATH /usr/share/go-1.7/
RUN GOPATH=/usr/share/go-1.7/ /usr/lib/go-1.7/bin/go get -u -v golang.org/x/tools/go/loader
