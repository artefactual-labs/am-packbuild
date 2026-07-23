ARG UV_VERSION=0.11.30
ARG UV_DIGEST=sha256:93b61e21202b1dab861092748e46bbd6e0e41dd84f59b9174efd2353186e1b47

FROM ghcr.io/astral-sh/uv:${UV_VERSION}@${UV_DIGEST} AS uv

FROM rockylinux:9

COPY --from=uv /uv /usr/local/bin/uv

RUN set -ex \
    && yum -y update \
    && yum -y install \
        epel-release \
        git \
        glibc-langpack-en \
        glibc-locale-source \
        langpacks-en \
        make \
        rpm-build \
        yum-utils \
    && yum clean all

RUN set -ex \
    localedef --no-archive -i en_US -f UTF-8 en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8


# Install node repo and build depends, to speed up the build process
RUN set -ex \
    && curl -fsSL https://rpm.nodesource.com/setup_24.x | bash -

RUN set -ex \
    && yum -y update \
    && yum -y install --enablerepo=crb \
        gcc \
        gcc-c++ \
        git \
        libffi-devel \
        libxslt-devel \
        mariadb-devel \
        nodejs \
        openldap-devel \
        openssl-devel \
        pkgconfig \
        postgresql-devel \
        python3.12-devel \
        python3-virtualenv \
    && yum clean all
