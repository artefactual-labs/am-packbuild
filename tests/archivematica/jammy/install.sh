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
elasticsearch_repo_version="${ELASTICSEARCH_PACKAGES_REPO_VERSION:-8.x}"
elasticsearch_package_version="${ELASTICSEARCH_PACKAGE_VERSION:-}"

dump_lowercase_environment_variables
echo "Using Archivematica packages repository version: ${packages_repo_version}"
echo "Using Elasticsearch packages repository version: ${elasticsearch_repo_version}"
if [ -n "${elasticsearch_package_version}" ]; then
    echo "Using Elasticsearch package version: ${elasticsearch_package_version}"
fi

export DEBIAN_FRONTEND=noninteractive
sudo debconf-set-selections <<< "postfix postfix/mailname string your.hostname.com"
sudo debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
sudo debconf-set-selections <<< "archivematica-storage-service archivematica-storage-service/dbconfig-install boolean true"
sudo debconf-set-selections <<< "archivematica-storage-service archivematica-storage-service/mysql/app-pass password demo-ss"
sudo debconf-set-selections <<< "archivematica-storage-service archivematica-storage-service/app-password-confirm password demo-ss"
sudo debconf-set-selections <<< "archivematica-mcp-server archivematica-mcp-server/dbconfig-install boolean true"
sudo debconf-set-selections <<< "archivematica-mcp-server archivematica-mcp-server/mysql/app-pass password demo-am"
sudo debconf-set-selections <<< "archivematica-mcp-server archivematica-mcp-server/app-password-confirm password demo-am"

configure_archivematica_apt_repos "${local_repository}" "${packages_repo_version}"

sudo apt-get -o Acquire::AllowInsecureRepositories=true update
sudo apt-get -y upgrade

sudo apt-get install -y openjdk-8-jre-headless mysql-server
sudo systemctl daemon-reload
sudo service mysql restart
sudo systemctl enable mysql

if [ "${search_enabled}" == "true" ] ; then
    install_elasticsearch_deb "${elasticsearch_repo_version}" "${elasticsearch_package_version}"
fi

sudo apt-get install -y --allow-unauthenticated archivematica-storage-service

sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/storage /etc/nginx/sites-enabled/storage

sudo apt-get install -y --allow-unauthenticated archivematica-mcp-server
if [ "${search_enabled}" != "true" ] ; then
    set_search_env_flags "/etc/default" "false" "mcp-server"
fi

sudo apt-get install -y --allow-unauthenticated archivematica-dashboard
if [ "${search_enabled}" != "true" ] ; then
    set_search_env_flags "/etc/default" "false" "dashboard"
fi

sudo apt-get install -y --allow-unauthenticated archivematica-mcp-client
if [ "${search_enabled}" != "true" ] ; then
    set_search_env_flags "/etc/default" "false" "mcp-client"
fi

sudo ln -sf /etc/nginx/sites-available/dashboard.conf /etc/nginx/sites-enabled/dashboard.conf

sudo service clamav-freshclam restart
sleep 120s
declare -a SERVICE_OPERATIONS=(
    "start clamav-daemon"
    "restart gearman-job-server"
    "start archivematica-mcp-server"
    "restart archivematica-mcp-client"
    "start archivematica-storage-service"
    "restart archivematica-dashboard"
    "restart nginx"
)

for operation in "${SERVICE_OPERATIONS[@]}"; do
    read -r action service <<<"${operation}"
    sudo service "${service}" "${action}"
done

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

run_archivematica_manage dashboard collectstatic --noinput --clear
run_archivematica_manage dashboard --chdir /opt/archivematica/archivematica compilemessages

run_archivematica_manage storage-service collectstatic --noinput --clear
run_archivematica_manage storage-service --chdir /opt/archivematica/archivematica-storage-service/ compilemessages
