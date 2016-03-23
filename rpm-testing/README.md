This Vagrant environment is based on the official CentOS 7 Vagrant box
`centos/7` which does not include the VirtualBox Guest Additions yet. While the
figure that out we are using the `rsync` mechanism provided by Vagrant to share
files with the virtual machine and giving it network access via
`public_network`.

The default behavior is to use the yum repo created in the `../rpm` directory
which needs to be previously built. This is set up inside the `Vagrantfile`
under the provisioning area. Alternatively, you can make use of our [public yum repository](https://docs.google.com/document/d/14VvpaMq0687BKqZnTUZC6ozHUXEFGMP1o0DXc59eosg/edit).
