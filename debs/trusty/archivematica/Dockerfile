FROM ubuntu:trusty


RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs

RUN wget -O /tmp/pip.py https://bootstrap.pypa.io/get-pip.py && python /tmp/pip.py

RUN wget -O - "http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0x36A76C6C49C29687" | apt-key add - 
RUN echo deb http://ppa.launchpad.net/spotify-jyrki/dh-virtualenv/ubuntu trusty main >> /etc/apt/sources.list

RUN wget -O - https://deb.nodesource.com/setup_8.x |  bash - 

ADD debian-dashboard/control /tmp/dashboard
ADD debian-MCPClient/control /tmp/mcpclient
ADD debian-MCPServer/control /tmp/mcpserver

RUN  apt-get update && \
     mkdir debian && \
     mv /tmp/dashboard debian/control && \
     yes  | mk-build-deps -i debian/control && \
     mv /tmp/mcpclient debian/control && \
     yes  | mk-build-deps -i debian/control && \
     mv /tmp/mcpserver debian/control && \
     yes  | mk-build-deps -i debian/control && \
     rm -rf debian



