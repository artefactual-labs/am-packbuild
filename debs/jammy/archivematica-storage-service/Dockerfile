ARG UV_VERSION=0.12.24
ARG UV_DIGEST=sha256:3af4716e991d6956a41e573eab705d0ee08500cd829ed30293eb8472f372c65a

FROM ghcr.io/astral-sh/uv:${UV_VERSION}@${UV_DIGEST} AS uv

FROM ubuntu:jammy

COPY --from=uv /uv /usr/local/bin/uv

ENV DEBIAN_FRONTEND=noninteractive

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
		rsync \
		software-properties-common \
	&& curl -sL https://deb.nodesource.com/setup_24.x | bash - && apt-get install -y nodejs \
	&& rm -rf /var/lib/apt/lists/*
