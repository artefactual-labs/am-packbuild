FROM ubuntu:jammy

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
	&& apt-get install -y \
		apt-transport-https \
		build-essential \
		debhelper \
		devscripts \
		dh-virtualenv \
		dpkg-dev \
		equivs \
		git \
		libffi-dev \
		libldap2-dev \
		libmysqlclient-dev \
		libsasl2-dev \
		libssl-dev \
		libxslt-dev \
		pkg-config \
        python3-dev \
		software-properties-common \
	&& curl -sL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs \
	&& rm -rf /var/lib/apt/lists/*
