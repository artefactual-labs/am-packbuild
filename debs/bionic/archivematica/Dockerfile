FROM ubuntu:bionic

RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs quilt apt-transport-https python-minimal

RUN wget -O /tmp/pip.py https://bootstrap.pypa.io/get-pip.py && python /tmp/pip.py

RUN wget -O - https://packages.archivematica.org/1.7.x/key.asc |\
    apt-key add - && \
    echo "deb [arch=amd64] http://packages.archivematica.org/1.7.x/ubuntu-externals xenial main" >> /etc/apt/sources.list


RUN apt-get update && apt-get install -y libffi-dev libssl-dev libxslt-dev dh-virtualenv python-dev dh-systemd libmysqlclient-dev libldap2-dev libsasl2-dev curl

RUN curl -sL https://deb.nodesource.com/setup_8.x |  bash - && apt-get install -y nodejs


