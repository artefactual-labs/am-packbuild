#!/bin/bash -e

#
# Install needed repos/keys
#
sudo wget -O - https://packages.archivematica.org/1.7.x/key.asc | sudo apt-key add -
#sudo sh -c 'echo "deb [arch=amd64] http://packages.archivematica.org/1.6.x/ubuntu trusty main" >> /etc/apt/sources.list'
sudo wget -O - http://jenkins-ci.archivematica.org/repos/devel.key | sudo apt-key add - 
sudo sh -c 'echo "deb [arch=amd64] http://packages.archivematica.org/1.7.x/ubuntu-externals trusty main" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb http://jenkins-ci.archivematica.org/repos/apt/release-0.11-trusty/ ./" >> /etc/apt/sources.list'
sudo wget -O - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
sudo sh -c 'echo "deb http://packages.elasticsearch.org/elasticsearch/1.7/debian stable main" >> /etc/apt/sources.list'

#
# Install requirements
#
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install git elasticsearch -y

#
# Install and configure ss
# 
sudo apt-get install -y archivematica-storage-service
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/storage /etc/nginx/sites-enabled/storage

#
# Add AM repo and install packages
# 
sudo sh -c 'echo deb http://jenkins-ci.archivematica.org/repos/apt/release-1.7-trusty/ ./ >> /etc/apt/sources.list'
sudo apt-get update

sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo apt-get install -y archivematica-mcp-server
sudo apt-get install -y archivematica-dashboard
sudo apt-get install -y archivematica-mcp-client
sudo ln -s /etc/nginx/sites-available/dashboard.conf /etc/nginx/sites-enabled/dashboard.conf

#
# Enable and start services
#
sudo service elasticsearch restart
sudo update-rc.d elasticsearch defaults 95 10

sudo freshclam
sudo service gearman-job-server restart
sudo service archivematica-mcp-server start
sudo service archivematica-mcp-client start
sudo service archivematica-storage-service start
sudo service archivematica-dashboard start
sudo service nginx restart
sudo service fits start
sudo service clamav-daemon start
