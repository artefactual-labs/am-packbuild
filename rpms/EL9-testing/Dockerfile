ARG TARGET=server
ARG DOCKER_IMAGE_NAME=rockylinux
ARG DOCKER_IMAGE_TAG=9

FROM rockylinux:9 AS install_rockylinux_9

RUN set -ex \
    && dnf -y update \
    && dnf -y install coreutils --allowerasing \
    && dnf -y install \
        glibc-langpack-en \
        openssh-server \
        python-unversioned-command \
        selinux-policy \
        sudo \
    && dnf clean all

FROM install_${DOCKER_IMAGE_NAME}_${DOCKER_IMAGE_TAG} as server

RUN useradd --home-dir /home/ubuntu --system ubuntu

RUN mkdir -p /etc/sudoers.d/ && echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/ubuntu

COPY --chown=ubuntu:ubuntu . /src

EXPOSE 22
EXPOSE 80
EXPOSE 8000

CMD [ "/sbin/init" ]

FROM ${TARGET}
