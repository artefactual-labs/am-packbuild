#!/bin/bash -eux

apt-get update -y
apt-get upgrade -y
apt-get install -y ansible git

echo '[defaults]' > /etc/ansible/ansible.cfg
echo 'allow_world_readable_tmpfiles = True' >> /etc/ansible/ansible.cfg

