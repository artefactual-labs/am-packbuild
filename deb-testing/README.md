This Vagrant environment is based on the official Ubuntu 18.04 Vagrant box
`ubuntu/1804` which does not include the VirtualBox Guest Additions yet. We will
be using the `vagrant-vbguest` plugin to make sure that they're installed
before we reach the provisioning stage.

### Instructions

Install the `vagrant-vbguest` plugin:

    $ vagrant plugin install vagrant-vbguest

Provision the Vagrant box using our official repository:

    $ vagrant up

Alternatively, provision the box using the local repository (`../debs`), which
needs to be previously built:

    # Build the packages and the local repo. Then create the box.
    $ make -C ../debs
    $ LOCAL_REPOSITORY="yes" vagrant up

Once is up you should be able to access to the web interfaces:

    - Access to Dashboard: http://192.168.33.2
    - Access to Storage Service: http://192.168.33.2:8000
