FROM ubuntu:trusty

# Intall required repos and dependencies
RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs quilt 

RUN wget -O /tmp/pip.py https://bootstrap.pypa.io/get-pip.py && python /tmp/pip.py

RUN wget -O - "http://keyserver.ubuntu.com:11371/pks/lookup?op=get&search=0x36A76C6C49C29687" | apt-key add - 
RUN echo deb http://ppa.launchpad.net/spotify-jyrki/dh-virtualenv/ubuntu trusty main >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y dh-virtualenv

RUN apt-get update && apt-get install -y libffi-dev libssl-dev libxslt-dev python-dev libmysqlclient-dev libldap2-dev libsasl2-dev curl

RUN curl -sL https://deb.nodesource.com/setup_8.x |  bash - && apt-get install -y nodejs

# Set Path
ENV PATH=/usr/local/bin:$PATH

# Update setuptools and virtualenv
RUN /usr/local/bin/pip install -U setuptools virtualenv
