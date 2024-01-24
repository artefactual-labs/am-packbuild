FROM rockylinux:8

# Environmnet variables needed during build

# Environment variables needed during runtime

RUN yum -y install rpm-build make git wget gcc-c++
RUN curl -fsSL https://rpm.nodesource.com/setup_14.x | bash -
RUN dnf -y install nodejs
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/rh/rh-nodejs8/root/bin/
