FROM rockylinux:9

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

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN set -ex \
    && yum -y update \
    && yum -y install --enablerepo=crb \
        gcc \
        gcc-c++ \
        git \
        libffi-devel \
        libxslt-devel \
        mariadb-devel \
        openldap-devel \
        openssl-devel \
        pkgconfig \
        postgresql-devel \
        python3-devel \
        python3-virtualenv \
    && yum clean all
