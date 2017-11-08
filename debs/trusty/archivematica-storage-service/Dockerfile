FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install -y dpkg-dev git build-essential wget debhelper \
    devscripts equivs quilt

RUN wget -O /tmp/pip.py https://bootstrap.pypa.io/get-pip.py && python /tmp/pip.py

# Dependencies are also obtained in the debian build script, this speeds up the process of building packages
RUN apt-get update &&  apt-get install -y libffi-dev libssl-dev libxslt-dev dh-virtualenv python-dev dh-systemd libmysqlclient-dev postgresql-server-dev-9.5

