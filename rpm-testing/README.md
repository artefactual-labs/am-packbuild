This Vagrant environment is based on the official CentOS 7 Vagrant box
`centos/7` which does not include the VirtualBox Guest Additions yet. We will
be using `rsync` file sharing and `public_network` connectivity for now.

You can provision the Vagrant box using the local yum repository in `../rpm`
that needs to be previously built or our official repository.

### Instructions

Provision the Vagrant box using our official repository:

```
$ vagrant up
```

Alternatively, provision the box using the local repository (`../rpm`), which
needs to be previously built:

```
$ REPOSITORY_CONFIG_FILE="archivematica-local.repo" vagrant up
```
