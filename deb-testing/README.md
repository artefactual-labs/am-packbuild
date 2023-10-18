This Vagrant environment is based on the official Ubuntu 22.04 Vagrant box
`ubuntu/jammy64`.

### Instructions

Provision the Vagrant box using our official repository:

    $ vagrant up

Alternatively, provision the box using the local repository (`../debs/jammy`),
which needs to be previously built:

    # Build the packages and the local repo. Then create the box.
    $ make -C ../debs/jammy
    $ LOCAL_REPOSITORY="yes" vagrant up

Once is up you should be able to access to the web interfaces:

    - Access to Dashboard: http://192.168.33.2
    - Access to Storage Service: http://192.168.33.2:8000
