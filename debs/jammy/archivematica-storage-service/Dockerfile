ARG UV_VERSION=0.11.30
ARG UV_DIGEST=sha256:93b61e21202b1dab861092748e46bbd6e0e41dd84f59b9174efd2353186e1b47

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
		python3-dev \
		rsync \
		software-properties-common \
	&& curl -sL https://deb.nodesource.com/setup_24.x | bash - && apt-get install -y nodejs \
	&& rm -rf /var/lib/apt/lists/*
