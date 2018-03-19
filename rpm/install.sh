#!/bin/bash -e

#
# Install needed repos/keys
#

sudo -u root rm -f /etc/yum.repos.d/archivematica-*.repo
sudo -u root bash -c 'cat << EOF > /etc/yum.repos.d/archivematica-dev.repo
[archivematica-dashboard]
name=archivematica-dashboard
baseurl=http://jenkins-ci.archivematica.org/repos/rpm/release-1.7
gpgcheck=0
enabled=1
[archivematica-ss]
name=archivematica-ss
baseurl=http://jenkins-ci.archivematica.org/repos/rpm/release-0.11
gpgcheck=0
enabled=1
[archivematica-extras]
name=archivematica-extras
baseurl=https://packages.archivematica.org/1.7.x/centos-extras
gpgcheck=0
enabled=1
EOF'

sudo -u root yum update -y
sudo -u root yum install -y epel-release

#
# Install additional repos
#

sudo -u root rpm -Uvh https://forensics.cert.org/cert-forensics-tools-release-el7.rpm
sudo -u root rpm -Uvh https://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
sudo -u root rpm --import https://packages.elastic.co/GPG-KEY-elasticsearch
sudo -u root bash -c 'cat << EOF > /etc/yum.repos.d/elasticsearch.repo
[elasticsearch-1.7]
name=Elasticsearch repository for 1.7 packages
baseurl=https://packages.elastic.co/elasticsearch/1.7/centos
gpgcheck=1
gpgkey=https://packages.elastic.co/GPG-KEY-elasticsearch
enabled=1
EOF'
#
# Install OpenJDK 8, Elasticsearch 1.7, MariaDB and Gearman
#

sudo -u root yum install -y java-1.8.0-openjdk-headless elasticsearch mariadb-server gearmand
sudo -u root systemctl enable elasticsearch
sudo -u root systemctl start elasticsearch
sudo -u root systemctl enable mariadb
sudo -u root systemctl start mariadb
sudo -u root systemctl enable gearmand
sudo -u root systemctl start gearmand


#
# Archivematica Storage Service
#

sudo -u root yum install -y python-pip archivematica-storage-service
sudo -u archivematica bash -c " \
     set -a -e -x
     source /etc/sysconfig/archivematica-storage-service
     cd /usr/lib/archivematica/storage-service
     /usr/share/python/archivematica-storage-service/bin/python manage.py migrate
";

sudo -u root systemctl enable archivematica-storage-service
sudo -u root systemctl start archivematica-storage-service
sudo -u root systemctl enable rngd
sudo -u root systemctl start rngd
sudo -u root systemctl enable nginx
sudo -u root systemctl start nginx

#
# Archivematica
#

sudo -u root yum install -y archivematica-common archivematica-mcp-server archivematica-mcp-client archivematica-dashboard python-six python-oletools

sudo -H -u root mysql -hlocalhost -uroot -e "DROP DATABASE IF EXISTS MCP; CREATE DATABASE MCP CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
sudo -H -u root mysql -hlocalhost -uroot -e "CREATE USER 'archivematica'@'localhost' IDENTIFIED BY 'demo';"
sudo -H -u root mysql -hlocalhost -uroot -e "GRANT ALL ON MCP.* TO 'archivematica'@'localhost';"

# Temporary fix
sudo -u root chown archivematica.archivematica /var/log/archivematica/dashboard -R
sudo -u archivematica bash -c " \
      set -a -e -x
      export $(cat /etc/sysconfig/archivematica-dashboard)
      cd /usr/share/archivematica/dashboard
      /usr/share/python/archivematica-dashboard/bin/python manage.py syncdb --noinput
 ";

sudo -u root systemctl enable archivematica-mcp-server
sudo -u root systemctl start archivematica-mcp-server
sudo -u root systemctl enable archivematica-mcp-client
sudo -u root systemctl start archivematica-mcp-client
sudo -u root systemctl enable archivematica-dashboard
sudo -u root systemctl start archivematica-dashboard
sudo -u root systemctl enable fits-nailgun
sudo -u root systemctl start fits-nailgun
sudo -u root systemctl restart nginx
sudo -u root sed -i 's/^#TCPSocket/TCPSocket/g' /etc/clamd.d/scan.conf 
sudo -u root sed -i 's/^Example//g' /etc/clamd.d/scan.conf
sudo -u root systemctl enable clamd@scan
sudo -u root systemctl start clamd@scan

# AM expects 7z to be named 7z
sudo ln -sf /usr/bin/7za /usr/bin/7z

# Configure firewall
sudo firewall-cmd --zone=public --add-port=81/tcp  --permanent
sudo firewall-cmd --zone=public --add-port=8001/tcp  --permanent
sudo service firewalld restart

# Print IP address after provisioning
ip addr | grep "dynamic eth1"

