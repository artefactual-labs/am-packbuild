#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -x

THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=tests/archivematica/common/helpers.sh
source "${THIS_DIR}/../common/helpers.sh"

search_enabled=$(get_env_boolean "SEARCH_ENABLED" "true")
local_repository=$(get_env_boolean "LOCAL_REPOSITORY" "false")
packages_repo_version="${ARCHIVEMATICA_PACKAGES_REPO_VERSION:-1.18.x}"
packages_repo_baseurl="${ARCHIVEMATICA_PACKAGES_REPO_BASEURL:-}"
elasticsearch_repo_version="${ELASTICSEARCH_PACKAGES_REPO_VERSION:-8.x}"
elasticsearch_package_version="${ELASTICSEARCH_PACKAGE_VERSION:-}"

dump_lowercase_environment_variables
echo "Using Archivematica packages repository version: ${packages_repo_version}"
if [ -n "${packages_repo_baseurl}" ]; then
    echo "Using Archivematica packages repository base URL: ${packages_repo_baseurl}"
fi
echo "Using Elasticsearch packages repository version: ${elasticsearch_repo_version}"
if [ -n "${elasticsearch_package_version}" ]; then
    echo "Using Elasticsearch package version: ${elasticsearch_package_version}"
fi


#
# Configure repository
#

configure_archivematica_yum_repos "${local_repository}" "${packages_repo_version}" "${packages_repo_baseurl}"

sudo -u root yum update -y
sudo -u root yum install -y epel-release policycoreutils-python-utils yum-utils
sudo -u root yum-config-manager --enable crb


#
# SELinux tweaks
#

if [ "$(getenforce)" != "Disabled" ]; then
    if ! sudo semanage port -m -t http_port_t -p tcp 80; then
        sudo semanage port -a -t http_port_t -p tcp 80
    fi
    if ! sudo semanage port -m -t http_port_t -p tcp 8000; then
        sudo semanage port -a -t http_port_t -p tcp 8000
    fi
    sudo setsebool -P httpd_can_network_connect_db=1
    sudo setsebool -P httpd_can_network_connect=1
    sudo setsebool -P httpd_setrlimit 1
fi


#
# Install MariaDB and Gearman
#

sudo -u root yum install -y java-1.8.0-openjdk-headless mariadb-server gearmand
sudo -u root systemctl enable mariadb
sudo -u root systemctl start mariadb
sudo -u root systemctl enable gearmand
sudo -u root systemctl start gearmand


if [ "${search_enabled}" == "true" ] ; then
    install_elasticsearch_rpm "${elasticsearch_repo_version}" "${elasticsearch_package_version}"
fi

#
# Archivematica Storage Service
#

sudo -H -u root mysql -hlocalhost -uroot -e "DROP DATABASE IF EXISTS SS; CREATE DATABASE SS CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
sudo -H -u root mysql -hlocalhost -uroot -e "DROP USER IF EXISTS 'archivematica'@'localhost';"
sudo -H -u root mysql -hlocalhost -uroot -e "CREATE USER 'archivematica'@'localhost' IDENTIFIED BY 'demo';"
sudo -H -u root mysql -hlocalhost -uroot -e "GRANT ALL ON SS.* TO 'archivematica'@'localhost';"

sudo -u root yum install -y archivematica-storage-service
run_archivematica_manage storage-service migrate

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

sudo -H -u root mysql -hlocalhost -uroot -e "DROP DATABASE IF EXISTS MCP; CREATE DATABASE MCP CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
sudo -H -u root mysql -hlocalhost -uroot -e "GRANT ALL ON MCP.* TO 'archivematica'@'localhost';"

run_archivematica_manage dashboard migrate --noinput

if [ "${search_enabled}" != "true" ] ; then
    set_search_env_flags "/etc/sysconfig" "${search_enabled}" "dashboard" "mcp-server"
fi

sudo -u root systemctl enable archivematica-mcp-server
sudo -u root systemctl start archivematica-mcp-server
sudo -u root systemctl enable archivematica-dashboard
sudo -u root systemctl start archivematica-dashboard

# Update nginx site configurations to match standard Archivematica ports
sudo -u root sed -i -e 's/80;/90;/g' /etc/nginx/nginx.conf
sudo -u root sed -i -e 's/listen 8001/listen 8000/g' /etc/nginx/conf.d/archivematica-storage-service.conf
sudo -u root sed -i -e 's/listen 81/listen 80/g' /etc/nginx/conf.d/archivematica-dashboard.conf
sudo -u root systemctl reload nginx

#
# MCPClient
#

sudo -u root yum install -y archivematica-mcp-client
sudo -u root sed -i 's/^#TCPSocket/TCPSocket/g' /etc/clamd.d/scan.conf
sudo -u root sed -i 's/^Example//g' /etc/clamd.d/scan.conf

if [ "${search_enabled}" != "true" ] ; then
    set_search_env_flags "/etc/sysconfig" "${search_enabled}" "mcp-client"
fi

sudo -u root systemctl enable archivematica-mcp-client
sudo -u root systemctl start archivematica-mcp-client
sudo -u root systemctl enable clamd@scan
sudo -u root systemctl start clamd@scan


#
# Set up the firewall
#

# We're adding the corresponding firewall rules only if the service is enabled
# and active. We can't add rules when the daemon is not running.
systemctl -q is-enabled firewalld || rc1=$?
systemctl -q is-active firewalld || rc2=$?
if [ "${rc1}" -eq 0 ] && [ "${rc2}" -eq 0 ]; then
    sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
    sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
    sudo systemctl restart firewalld || true
fi

run_archivematica_manage storage-service create_user \
    --username=admin \
    --password=archivematica \
    --email="example@example.com" \
    --api-key="apikey" \
    --superuser

run_archivematica_manage dashboard install \
    --username="admin" \
    --password="archivematica" \
    --email="example@example.com" \
    --org-name="test" \
    --org-id="test" \
    --api-key="apikey" \
    --ss-url="http://localhost:8000" \
    --ss-user="admin" \
    --ss-api-key="apikey" \
    --site-url="http://localhost"

if ! dashboard_code_dir=$(
    first_existing_dir \
        /opt/archivematica/archivematica \
        /usr/share/archivematica/dashboard \
        /usr/lib/archivematica/dashboard
); then
    echo "Unable to locate dashboard source directory" >&2
    exit 1
fi

run_archivematica_manage dashboard collectstatic --noinput --clear
run_archivematica_manage dashboard --chdir "${dashboard_code_dir}" compilemessages

if ! storage_service_code_dir=$(
    first_existing_dir \
        /opt/archivematica/archivematica-storage-service \
        /usr/share/archivematica/storage-service \
        /usr/lib/archivematica/storage-service
); then
    echo "Unable to locate storage service source directory" >&2
    exit 1
fi

run_archivematica_manage storage-service collectstatic --noinput --clear
run_archivematica_manage storage-service --chdir "${storage_service_code_dir}" compilemessages
