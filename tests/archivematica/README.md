# Instructions

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Software requirements](#software-requirements)
- [Set up a Python virtual environment](#set-up-a-python-virtual-environment)
- [Set up EL9 packages](#set-up-el9-packages)
  - [Install EL9 packages from archivematica.org](#install-el9-packages-from-archivematicaorg)
  - [Install EL9 packages from a local repository](#install-el9-packages-from-a-local-repository)
  - [Upgrade EL9 packages from archivematica.org](#upgrade-el9-packages-from-archivematicaorg)
  - [Upgrade EL9 packages from a local repository](#upgrade-el9-packages-from-a-local-repository)
  - [Install EL9 packages with Ansible](#install-el9-packages-with-ansible)
- [Set up Ubuntu 22.04 Jammy packages](#set-up-ubuntu-2204-jammy-packages)
  - [Install jammy packages from archivematica.org](#install-jammy-packages-from-archivematicaorg)
  - [Install jammy packages from a local repository](#install-jammy-packages-from-a-local-repository)
  - [Upgrade jammy packages from archivematica.org](#upgrade-jammy-packages-from-archivematicaorg)
  - [Upgrade jammy packages from a local repository](#upgrade-jammy-packages-from-a-local-repository)
- [Test the Archivematica installation](#test-the-archivematica-installation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Software requirements

- Podman
- Python 3

This environment has been tested with Podman 3.4.4 and podman-compose 1.6.0 and
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

### Upgrade EL9 packages from archivematica.org

Keep the same running container for both steps: install the release you want to
upgrade _from_, then execute the upgrade script pointing at the release you
want to validate. Swap the version numbers to match the scenario you're testing.
Archivematica 1.17.x packages rely on Elasticsearch 6.x, while Archivematica
1.18.x (and newer) use Elasticsearch 8.x. The install and upgrade scripts honor
`ELASTICSEARCH_PACKAGES_REPO_VERSION` and `ELASTICSEARCH_PACKAGE_VERSION`, so
set them explicitly any time you need a non-default combination.

```shell
# Example: install 1.17.x as the baseline (Elasticsearch 6.x)
podman-compose exec \
    --env ARCHIVEMATICA_PACKAGES_REPO_VERSION=1.17.x \
    --env ELASTICSEARCH_PACKAGES_REPO_VERSION=6.x \
    --user ubuntu \
    archivematica /am-packbuild/tests/archivematica/EL9/install.sh

# Upgrade that container to 1.18.x (Elasticsearch 8.x)
podman-compose exec \
    --env ARCHIVEMATICA_PACKAGES_REPO_VERSION=1.18.x \
    --env ELASTICSEARCH_PACKAGES_REPO_VERSION=8.x \
    --user ubuntu \
    archivematica /am-packbuild/tests/archivematica/EL9/upgrade.sh
```

### Upgrade EL9 packages from a local repository

Build the local RPM repository as shown above. Install your baseline packages
from whichever source you prefer (published repos or a previous local build),
then rerun the upgrade with `LOCAL_REPOSITORY="yes"` so `upgrade.sh` pulls the
new bits from `/am-packbuild/rpms/EL9/_yum_repository`. Remember to set
`ELASTICSEARCH_PACKAGES_REPO_VERSION=6.x` when installing 1.17.x as the
baseline, and switch it to `8.x` (or whichever version you are validating) for
the upgrade.

```shell
podman-compose exec \
    --env LOCAL_REPOSITORY="yes" \
    --env ARCHIVEMATICA_PACKAGES_REPO_VERSION=1.18.x \
    --env ELASTICSEARCH_PACKAGES_REPO_VERSION=8.x \
    --user ubuntu \
    archivematica /am-packbuild/tests/archivematica/EL9/upgrade.sh
```

### Install EL9 packages with Ansible

Test using a local repository built from the `/rpms/EL9` directory of this
repository using Ansible.

Create the local repository:

```shell
make -C ../../rpms/EL9/archivematica
make -C ../../rpms/EL9/archivematica-storage-service
make -C ../../rpms/EL9 createrepo
```

Install Ansible:

```shell
python3 -m pip install ansible
```

Install the playbook requirements:

```shell
ansible-galaxy install -f -p EL9/ansible/roles/ -r EL9/ansible/requirements.yml
```

Copy your SSH public key to the container:

```shell
podman-compose exec -u root archivematica bash -c 'mkdir -p /home/ubuntu/.ssh'
podman cp $HOME/.ssh/id_rsa.pub archivematica-package-testing_archivematica_1:/home/ubuntu/.ssh/authorized_keys
podman-compose exec -u root archivematica bash -c 'chown -R ubuntu:ubuntu /home/ubuntu/'
```

Run the Archivematica installation playbook:

```shell
export ANSIBLE_HOST_KEY_CHECKING=False
export ANSIBLE_REMOTE_PORT=2222
ansible-playbook -i localhost, EL9/ansible/playbook.yml \
    -u ubuntu \
    -v
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

### Upgrade jammy packages from archivematica.org

Just like on EL9, reuse the same container: install the source release, then run
`upgrade.sh` with the repository version that contains the packages you want to
test. Match the Elasticsearch repository to the Archivematica version you're
testing—1.17.x needs Elasticsearch 6.x, while 1.18.x uses 8.x.

```shell
# Install the baseline release (example: 1.17.x, Elasticsearch 6.x)
podman-compose exec \
    --env ARCHIVEMATICA_PACKAGES_REPO_VERSION=1.17.x \
    --env ELASTICSEARCH_PACKAGES_REPO_VERSION=6.x \
    --user ubuntu \
    archivematica /am-packbuild/tests/archivematica/jammy/install.sh

# Upgrade to the candidate release (example: 1.18.x, Elasticsearch 8.x)
podman-compose exec \
    --env ARCHIVEMATICA_PACKAGES_REPO_VERSION=1.18.x \
    --env ELASTICSEARCH_PACKAGES_REPO_VERSION=8.x \
    --user ubuntu \
    archivematica /am-packbuild/tests/archivematica/jammy/upgrade.sh
```

### Upgrade jammy packages from a local repository

Create the local APT repository first. When you are ready to test the new
packages, run the upgrade with `LOCAL_REPOSITORY="yes"` so the script points
APT at `/am-packbuild/debs/jammy/_deb_repository`. Use
`ELASTICSEARCH_PACKAGES_REPO_VERSION` to ensure the right Elasticsearch release
is installed at each step (e.g., 6.x for 1.17.x installs and 8.x for 1.18.x
upgrades).

```shell
podman-compose exec \
    --env LOCAL_REPOSITORY="yes" \
    --env ARCHIVEMATICA_PACKAGES_REPO_VERSION=1.18.x \
    --env ELASTICSEARCH_PACKAGES_REPO_VERSION=8.x \
    --user ubuntu \
    archivematica /am-packbuild/tests/archivematica/jammy/upgrade.sh
```

## Test the Archivematica installation

Once installation finishes you should be able to access to the web interfaces:

- Access to Dashboard: <http://localhost:8000>
- Access to Storage Service: <http://localhost:8001>
