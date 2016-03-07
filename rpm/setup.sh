#!/bin/bash

echo "Provisioning virtual machine..."
yum install -y epel-release
sleep 5s
yum install -y  git gcc libffi-devel openssl-devel libxslt-devel rpm-build make vim mariadb-server

systemctl enable mariadb
systemctl start mariadb
echo 'create database MCP;' | mysql
echo 'create user "archivematica"@"localhost" identified by "demo";' | mysql
echo 'grant all on MCP.* to  "archivematica"@"localhost";' | mysql

#echo "Clean old rpms"
#make rpm-clean

echo "Build rpms"
cd /vagrant/
chown root.root . -R
make 
yum --nogpg localinstall -y archivematica-storage-service*.rpm
yum --nogpg localinstall -y archivematica-common*.rpm archivematica-mcp-server*.rpm archivematica-mcp-client*.rpm

echo "Populate MCP database and start gearmand"
cat /usr/share/archivematica/mysql | mysql MCP
systemctl enable gearmand
systemctl start gearmand

echo "Install dashboard"
yum --nogpg localinstall -y archivematica-dashboard*.rpm

echo "Enable and start mcp-server and client"
systemctl enable archivematica-mcp-server
systemctl enable archivematica-mcp-client
systemctl start archivematica-mcp-server
systemctl start archivematica-mcp-client

echo "Replace clamdscan with clamscan"
cp /usr/bin/clamdscan{,.orig}
cp /usr/bin/clamscan{,.orig}
/bin/cp /usr/bin/clamscan /usr/bin/clamdscan
sed -i 's/80/81/g' /etc/nginx/nginx.conf
echo "Start services"
httpd
nginx -c /etc/nginx/nginx.conf
uwsgi --plugin python /etc/uwsgi.d/storage.ini > /dev/null 2>&1
#Open firewall ports
service firewalld stop

