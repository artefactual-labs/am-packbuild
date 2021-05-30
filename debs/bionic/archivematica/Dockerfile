FROM ubuntu:bionic

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
        && apt-get install -y \
                dpkg-dev \
                git \
                build-essential \
                debhelper \
                devscripts \
                equivs \
                apt-transport-https \
                python3.6-dev \
                python3.6-distutils \
                libffi-dev \
                libssl-dev \
                libxslt-dev \
                dh-systemd \
                libmysqlclient-dev \
                libldap2-dev \
                libsasl2-dev \
        && update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1 \
        && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 \
        && curl -s https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && python /tmp/get-pip.py \
	&& curl -sL https://deb.nodesource.com/setup_8.x | bash - && apt-get install -y nodejs

# Install recent version of dh-virtualenv.
RUN apt-get install -y software-properties-common \
	&& add-apt-repository ppa:jyrki-pulliainen/dh-virtualenv \
	&& apt-get update \
	&& apt-get install -y dh-virtualenv
