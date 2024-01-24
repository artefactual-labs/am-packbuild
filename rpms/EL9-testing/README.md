# Instructions

This Vagrant environment is based on the official Rocky Linux 9 Vagrant box
`rockylinux/9`.

Provision the Vagrant box using our official repository:

    vagrant up

Alternatively, provision the box using the local repository (`../EL9`),
which needs to be previously built:

    # Build the packages and the local repo. Then create the box.
    $ make -C ../EL9
    $ LOCAL_REPOSITORY="yes" vagrant up

Once is up you should be able to access to the web interfaces:

    - Access to Dashboard: http://192.168.33.2:81.
    - Access to Storage Service: http://192.168.33.2:8001.
