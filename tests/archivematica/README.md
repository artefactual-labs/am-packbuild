# Instructions

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Software requirements](#software-requirements)
- [Set up a Python virtual environment](#set-up-a-python-virtual-environment)
- [Set up EL9 packages](#set-up-el9-packages)
  - [Install EL9 packages from archivematica.org](#install-el9-packages-from-archivematicaorg)
  - [Install EL9 packages from a local repository](#install-el9-packages-from-a-local-repository)
- [Set up Ubuntu 22.04 Jammy packages](#set-up-ubuntu-2204-jammy-packages)
  - [Install jammy packages from archivematica.org](#install-jammy-packages-from-archivematicaorg)
  - [Install jammy packages from a local repository](#install-jammy-packages-from-a-local-repository)
- [Test the Archivematica installation](#test-the-archivematica-installation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Software requirements

- Podman
- crun >= 1.14.4
- Python 3

This environment has been tested with Podman 3.4.4 and podman-compose 1.1.0 and
it is based on the official Docker images:

- rockylinux:9
- ubuntu:22.04

## Set up a Python virtual environment

Create a virtual environment and activate it:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python requirements:

```shell
python3 -m pip install -r requirements.txt
```

## Set up EL9 packages

Start the Compose environment:

```shell
export DOCKER_IMAGE_NAME=rockylinux
export DOCKER_IMAGE_TAG=9
podman-compose up --detach
```

### Install EL9 packages from archivematica.org

Install `EL9` packages from the published Archivematica repository:

```shell
podman-compose exec --user ubuntu archivematica /am-packbuild/tests/archivematica/EL9/install.sh
```

### Install EL9 packages from a local repository

Alternatively, test using a local repository built from the `/rpms/EL9`
directory of this repository.

Create the local repository:

```shell
make -C ../../rpms/EL9/archivematica
make -C ../../rpms/EL9/archivematica-storage-service
make -C ../../rpms/EL9 createrepo
```

Install `EL9` packages using the local repository:

```shell
podman-compose exec --env LOCAL_REPOSITORY="yes" --user ubuntu archivematica /am-packbuild/tests/archivematica/EL9/install.sh
```

## Set up Ubuntu 22.04 Jammy packages

Start the Compose environment:

```shell
export DOCKER_IMAGE_NAME=ubuntu
export DOCKER_IMAGE_TAG=22.04
podman-compose up --detach
```

### Install jammy packages from archivematica.org

Install `jammy` packages from the published Archivematica repository:

```shell
podman-compose exec --user ubuntu archivematica /am-packbuild/tests/archivematica/jammy/install.sh
```

### Install jammy packages from a local repository

Alternatively, test using a local repository built from the `/debs/jammy`
directory of this repository.

Create the local repository:

```shell
make -C ../../debs/jammy/archivematica
make -C ../../debs/jammy/archivematica-storage-service
make -C ../../debs/jammy createrepo
```

Install `jammy` packages using the local repository:

```shell
podman-compose exec --env LOCAL_REPOSITORY="yes" --user ubuntu archivematica /am-packbuild/tests/archivematica/jammy/install.sh
```

## Test the Archivematica installation

Once installation finishes you should be able to access to the web interfaces:

- Access to Dashboard: <http://localhost:8000>
- Access to Storage Service: <http://localhost:8001>
