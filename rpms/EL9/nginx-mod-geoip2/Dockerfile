FROM rockylinux:9

# Declare the build argument
ARG VERSION

# Make the variable accessible in all commands
ENV VERSION=${VERSION}

RUN dnf install -y epel-release && \
    dnf config-manager --set-enabled crb && \
    dnf groupinstall -y "Development Tools" && \
    dnf install -y rpm-build rpmdevtools dnf-plugins-core nginx-${VERSION} nginx-mod-devel-${VERSION} libmaxminddb-devel rpm-build make git wget gcc
