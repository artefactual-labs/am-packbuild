#!/bin/bash
# Start mysql
service mysql start
#echo 'CREATE USER "archivematica"@"localhost" IDENTIFIED BY "demo";' | mysql
#echo 'CREATE DATABASE MCP;' | mysql
#echo 'GRANT ALL PRIVILEGES on MCP.* to "archivematica"@"localhost";' | mysql
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure archivematica-mcp-server
dpkg-reconfigure archivematica-dashboard

#Check if we have a seed and load it
if [ -a /seed/storage.db ]
        then
        cp /seed/storage.db /var/archivematica/storage-service/storage.db
        fi
if [ -a /seed/seed.sql ]
        then
        cat /seed/seed.sql | mysql MCP
fi

### Start services
service clamav-daemon start
service gearman-job-server start
service elasticsearch start
service nginx start
service uwsgi start
/usr/bin/supervisord -n 
