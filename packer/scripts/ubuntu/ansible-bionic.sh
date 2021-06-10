#!/bin/bash -eux

apt-get update -y
apt-get upgrade -y
apt-get install -y python-dev curl git net-tools acl

curl -s https://bootstrap.pypa.io/pip/2.7/get-pip.py | python2.7
pip install ansible==2.9.10 jmespath

mkdir -p /etc/ansible

cat << EOF
[defaults]
allow_world_readable_tmpfiles = True

[ssh_connection]
pipelining = True
EOF
