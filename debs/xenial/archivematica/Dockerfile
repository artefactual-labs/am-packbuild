FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs

RUN wget -O /tmp/pip.py https://bootstrap.pypa.io/get-pip.py && python /tmp/pip.py

RUN wget -O - https://deb.nodesource.com/setup_8.x |  bash -

ADD debian-dashboard/control /tmp/dashboard
ADD debian-MCPClient/control /tmp/mcpclient
ADD debian-MCPServer/control /tmp/mcpserver

RUN  apt-get update && \
     mkdir debian && \
     cp /tmp/dashboard debian/control && \
     yes  | mk-build-deps -i debian/control && \
     cp /tmp/mcpclient debian/control && \
     yes  | mk-build-deps -i debian/control && \
     cp /tmp/mcpserver debian/control && \
     yes  | mk-build-deps -i debian/control 
