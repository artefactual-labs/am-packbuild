# Packer templates

## Requirements

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) 7.1 or higher
- [Packer](https://developer.hashicorp.com/packer/install) 1.12 or higher
- [Vagrant](https://developer.hashicorp.com/vagrant/install) 2.4.3 or higher

## How to build the Ubuntu base template

- Clone this repository

```shell
git clone https://github.com/artefactual-labs/am-packbuild
```

- Change to the Ubuntu base template directory

```shell
cd packer/templates/vagrant-base-ubuntu-amd64
```

- Run packer

To enable detailed logging, set the `PACKER_LOG` environment variable to `1`.

There are variables files for different Ubuntu versions. Specify the version
you need as a base using the `-var-file` option in the build command.

```shell
packer init template.json.pkr.hcl
packer build -var-file=ubuntu-24.04.pkvars.hcl template.json.pkr.hcl
```

## Archivematica Vagrant box

- Build the `vagrant-base-ubuntu-amd64` base template as explained above.

- Change to the Archivematica box directory:

```shell
cd packer/templates/vagrant-box-archivematica
```

- Run packer

To enable detailed logging, set the `PACKER_LOG` environment variable to `1`.

```shell
packer init template.json.pkr.hcl
packer build template.json.pkr.hcl
```

## AtoM Vagrant box

- Build the `vagrant-base-ubuntu-amd64` base template as explained above.

- Change to the AtoM box directory:

```shell
cd packer/templates/vagrant-box-archivematica
```

- Run packer

To enable detailed logging, set the `PACKER_LOG` environment variable to `1`.

```shell
packer init template.json.pkr.hcl
packer build template.json.pkr.hcl
```
