#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -x


function get_env_boolean() {
    local name="$1"
    local default="$2"
    local ret="${default}"
    if [ "${default}" == "true" ]; then
        if [ "${!name}" == "no" ] || [ "${!name}" == "false" ] || [ "${!name}" == "0" ]; then
            ret="false"
        fi
    fi
    if [ "${default}" == "false" ]; then
        if [ "${!name}" == "yes" ] || [ "${!name}" == "true" ] || [ "${!name}" == "1" ]; then
            ret="true"
        fi
    fi
    echo -n "${ret}"
}

search_enabled=$(get_env_boolean "SEARCH_ENABLED" "true")
local_repository=$(get_env_boolean "LOCAL_REPOSITORY" "false")

echo "~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~"
while read -r line; do echo "$line=${!line}"; done < <(compgen -v | grep -v '[^[:lower:]_]' | grep -v '^_$')
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


#
# Configure repository
#

if [ "${local_repository}" == "true" ] ; then
    sudo -u root bash -c 'cat << EOF > /etc/yum.repos.d/archivematica.repo
[archivematica]
name=archivematica
baseurl=file:///am-packbuild/rpms/EL9/_yum_repository/
enabled=1
gpgcheck=0
EOF'
else
    sudo -u root bash -c 'cat << EOF > /etc/yum.repos.d/archivematica.repo
[archivematica]
name=archivematica
baseurl=https://packages.archivematica.org/1.15.x/rocky9
gpgcheck=1
gpgkey=https://packages.archivematica.org/1.15.x/key.asc
enabled=1
EOF'
fi

sudo -u root bash -c 'cat << EOF >> /etc/yum.repos.d/archivematica.repo
[archivematica-extras]
name=archivematica-extras
baseurl=https://packages.archivematica.org/1.15.x/rocky9-extras
gpgcheck=1
gpgkey=https://packages.archivematica.org/1.15.x/key.asc
enabled=1
EOF'

sudo -u root yum update -y
sudo -u root yum install -y epel-release policycoreutils-python-utils


#
# SELinux tweaks
#

if [ $(getenforce) != "Disabled" ]; then
    sudo semanage port -m -t http_port_t -p tcp 81
    sudo semanage port -a -t http_port_t -p tcp 8001
    sudo setsebool -P httpd_can_network_connect_db=1
    sudo setsebool -P httpd_can_network_connect=1
    sudo setsebool -P httpd_setrlimit 1
fi


#
# Install MariaDB and Gearman
#

sudo -u root yum install -y --enablerepo=crb mariadb-server gearmand
sudo -u root systemctl enable mariadb
sudo -u root systemctl start mariadb
sudo -u root systemctl enable gearmand
sudo -u root systemctl start gearmand


if [ "${search_enabled}" == "true" ] ; then
    sudo -u root rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
    sudo -u root bash -c 'cat << EOF > /etc/yum.repos.d/elasticsearch.repo
[elasticsearch-6.x]
name=Elasticsearch repository for 6.x packages
baseurl=https://artifacts.elastic.co/packages/6.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF'
    sudo -u root yum install -y java-1.8.0-openjdk-headless elasticsearch
    sudo -u root systemctl enable elasticsearch
    sudo -u root systemctl start elasticsearch
fi

#
# Archivematica Storage Service
#

sudo -H -u root mysql -hlocalhost -uroot -e "DROP DATABASE IF EXISTS SS; CREATE DATABASE SS CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
sudo -H -u root mysql -hlocalhost -uroot -e "CREATE USER 'archivematica'@'localhost' IDENTIFIED BY 'demo';"
sudo -H -u root mysql -hlocalhost -uroot -e "GRANT ALL ON SS.* TO 'archivematica'@'localhost';"

sudo -u root yum install -y archivematica-storage-service
sudo -u archivematica bash -c " \
  set -a -e -x
  source /etc/sysconfig/archivematica-storage-service
  cd /usr/lib/archivematica/storage-service
  /usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/python manage.py migrate
";

sudo -u root systemctl enable archivematica-storage-service
sudo -u root systemctl start archivematica-storage-service
sudo -u root systemctl enable nginx
sudo -u root systemctl start nginx
sudo -u root systemctl enable rngd
sudo -u root systemctl start rngd


#
# Dashboard and MCPServer
#

sudo -u root yum clean all
sudo -u root yum install -y archivematica-common archivematica-mcp-server archivematica-dashboard

sudo -H -u root mysql -hlocalhost -uroot -e "DROP DATABASE IF EXISTS MCP; CREATE DATABASE MCP CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
sudo -H -u root mysql -hlocalhost -uroot -e "GRANT ALL ON MCP.* TO 'archivematica'@'localhost';"

sudo -u archivematica bash -c " \
  set -a -e -x
  source /etc/sysconfig/archivematica-dashboard
  cd /usr/share/archivematica/dashboard
  /usr/share/archivematica/virtualenvs/archivematica/bin/python manage.py migrate --noinput
";

sudo -u root bash -c "echo 'ARCHIVEMATICA_DASHBOARD_DASHBOARD_SEARCH_ENABLED=${search_enabled}' >> /etc/sysconfig/archivematica-dashboard"
sudo -u root bash -c "echo 'ARCHIVEMATICA_MCPSERVER_MCPSERVER_SEARCH_ENABLED=${search_enabled}' >> /etc/sysconfig/archivematica-mcp-server"

sudo -u root systemctl enable archivematica-mcp-server
sudo -u root systemctl start archivematica-mcp-server
sudo -u root systemctl enable archivematica-dashboard
sudo -u root systemctl start archivematica-dashboard
sudo -u root systemctl reload nginx


#
# MCPClient
#

sudo -u root yum install -y archivematica-mcp-client
sudo -u root sed -i 's/^#TCPSocket/TCPSocket/g' /etc/clamd.d/scan.conf
sudo -u root sed -i 's/^Example//g' /etc/clamd.d/scan.conf
sudo -u root bash -c "echo 'ARCHIVEMATICA_MCPCLIENT_MCPCLIENT_SEARCH_ENABLED=${search_enabled}' >> /etc/sysconfig/archivematica-mcp-client"

sudo -u root systemctl enable archivematica-mcp-client
sudo -u root systemctl start archivematica-mcp-client
sudo -u root systemctl enable fits-nailgun
sudo -u root systemctl start fits-nailgun
sudo -u root systemctl enable clamd@scan
sudo -u root systemctl start clamd@scan


#
# Set up the firewall
#

# We're adding the corresponding firewall rules only if the service is enabled
# and active. We can't add rules when the daemon is not running.
systemctl -q is-enabled firewalld || rc1=$?
systemctl -q is-active firewalld || rc2=$?
if [ ${rc1} -eq 0 ] && [ ${rc2} -eq 0 ]; then
    sudo firewall-cmd --zone=public --add-port=81/tcp --permanent
    sudo firewall-cmd --zone=public --add-port=8001/tcp --permanent
    sudo systemctl restart firewalld || true
fi
