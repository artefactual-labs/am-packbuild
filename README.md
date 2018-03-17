### Build packages

You need Docker installed and running.

CentOS 7 packages:

    make -C rpm

This also builds a local repository that you can use later from `rpm-testing`.

We don't have a single target yet for Xenial/Trusty packages but you can build
the packages individually, for example:

    make -C debs/xenial/archivematica
    make -C debs/xenial/archivematica-storage-service

### Test packages

CentOS 7 packages: see the [./rpm-testing](rpm-testing) directory for more details.

Ubuntu packages: this is work in progress (see #127).
