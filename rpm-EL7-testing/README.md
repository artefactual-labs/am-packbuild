# Instructions

This Vagrant environment is based on the official CentOS 7 Vagrant box
`centos/7` which does not include the VirtualBox Guest Additions yet. We will
be using the `vagrant-vbguest` plugin to make sure that they're installed
before we reach the provisioning stage.

Install the `vagrant-vbguest` plugin:

    vagrant plugin install vagrant-vbguest

Provision the Vagrant box using our official repository:

    vagrant up

Alternatively, provision the box using the local repository (`../rpm-EL7`), which
needs to be previously built:

    # Build the packages and the local repo. Then create the box.
    $ make -C ../rpm-EL7 
    $ LOCAL_REPOSITORY="yes" vagrant up

Once is up you should be able to access to the web interfaces:

    - Access to Dashboard: http://192.168.33.2:81.
    - Access to Storage Service: http://192.168.33.2:8001.
