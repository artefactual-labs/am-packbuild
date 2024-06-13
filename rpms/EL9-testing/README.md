# Instructions

## Software requirements

- Podman
- crun >= 1.14.4
- Python 3

This environment has been tested with Podman 3.4.4 and podman-compose 1.1.0
and is based on the official `rockylinux:9` Docker image.

## Set up

Create a virtual environment and activate it:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python requirements:

```shell
python3 -m pip install -r requirements.txt
```

## Starting the Compose environment

Start the Compose services:

```shell
podman-compose up --detach
```

## Test installing packages

Test packages from the published Archivematica repository:

```shell
podman-compose exec --user ubuntu archivematica /am-packbuild/rpms/EL9-testing/install.sh
```

Alternatively, test using the local repository (`../EL9`), which needs to be
previously built:

```shell
make -C ../EL9
```

Test using the local repository:

```shell
podman-compose exec --env LOCAL_REPOSITORY="yes" --user ubuntu archivematica /am-packbuild/rpms/EL9-testing/install.sh
```

Once installation finishes you should be able to access to the web interfaces:

- Access to Dashboard: <http://localhost:8000>
- Access to Storage Service: <http://localhost:8001>
