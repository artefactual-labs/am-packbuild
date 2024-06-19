ARG TARGET=server
ARG DOCKER_IMAGE_NAME=ubuntu
ARG DOCKER_IMAGE_TAG=22.04

FROM ubuntu:22.04 AS install_ubuntu_22.04

ENV DEBIAN_FRONTEND noninteractive

RUN set -ex \
	&& apt-get update \
	&& apt-get install -y \
        curl \
        dialog \
        gnupg \
        locales \
        openssh-server \
        rsync \
        sudo \
    && apt-get clean

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TZ=UTC

FROM install_${DOCKER_IMAGE_NAME}_${DOCKER_IMAGE_TAG} as server

RUN useradd --home-dir /home/ubuntu --system ubuntu

RUN mkdir -p /etc/sudoers.d/ && echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/ubuntu

RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

COPY --chown=ubuntu:ubuntu . /src

EXPOSE 22
EXPOSE 80
EXPOSE 8000

CMD [ "/sbin/init" ]

FROM ${TARGET}
