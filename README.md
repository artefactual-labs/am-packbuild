### Build packages

You need Docker installed and running.

CentOS 7 packages:

    make -C rpm

This also builds a local repository that you can use later from `rpm-testing`.

We don't have a single target yet for Xenial/Trusty packages but you can build
the packages individually, for example:

    make -C debs/xenial/archivematica
    make -C debs/xenial/archivematica-storage-service

#### Using parameters

Most makefiles support parameters in the format of environment variables. They 
may be a bit different between packages, but the most common are:
    BRANCH
    VERSION
    RELEASE

So in order to build an specific branch / version, this command can be used from
the folder of the package we want to build:

    make BRANCH=qa/1.x VERSION=1.7.0 RELEASE=rc5

Have in mind that the Makefiles are a bit recursive, they will invoke docker, 
mount the current folder, and run the deb-build target.

#### Development

Some makefiles have a "dev" target, that give you a shell inside of the docker 
used to build packages. When you are inside the container, the command needed to
build packages is:

    make deb-build

### Repositories management

This repo generates Archivematica packages, but also packages that need to be 
installed in order for Archivematica to run. They are placed in the 
ubuntu-extras or centos-extras repos.

In order to add a package to a repo, once its built and uploaded to a temporary folder at https://packages.archivematica.org, the steps are:

For centos packages:

  - Copy the rpm into centos-extras repo
  - Run ``createrepo``
  - Run '``gpg --detach-sign --armor repodata/repomd.xml`` to sign the 
repository contents

For debian packages:

  - Upload the package to packages.archivematica.org
  - Go to the repository folder ( mnt/st-sites-pub/packages.archivematica.org/1.7.x/ubuntu-externals )
  - Add the packages with

     ``reprepro includedeb trusty /path/to/packages/*.deb``
     ``reprepro includedsc trusty /path/to/packages/*.deb``

This needs to be repeated for each ubuntu release and package. More info about 
about managing debian repositories using reprepro can be found [https://wiki.archivematica.org/Release_Process#Build_deb.2Frpm_packages](here)


### Test package
CentOS 7 packages: see the [./rpm-testing](rpm-testing) directory for more details.

Ubuntu packages: this is work in progress (see #127).
