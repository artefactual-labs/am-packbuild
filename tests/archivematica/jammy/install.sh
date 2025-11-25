#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -x

THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=tests/archivematica/common/helpers.sh
source "${THIS_DIR}/../common/helpers.sh"

wait_for_service_active() {
    local service="$1"
    local timeout="${2:-120}"
    local interval="${3:-5}"
    local elapsed=0

    until sudo systemctl is-active --quiet "${service}"; do
        if [ "${elapsed}" -ge "${timeout}" ]; then
            echo "Service ${service} did not become active within ${timeout}s" >&2
            return 1
        fi
        sleep "${interval}"
        elapsed=$((elapsed + interval))
    done
}

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

if [ "${local_repository}" == "true" ]; then
    sudo apt-get -o Acquire::AllowInsecureRepositories=true update
else
    sudo apt-get update
fi
sudo apt-get -y upgrade

sudo apt-get install -y openjdk-8-jre-headless mysql-server
sudo systemctl daemon-reload
sudo service mysql restart
sudo systemctl enable mysql

if [ "${search_enabled}" == "true" ] ; then
    install_elasticsearch_deb "${elasticsearch_repo_version}" "${elasticsearch_package_version}" "${local_repository}"
fi

apt_auth_flags=()
if [ "${local_repository}" == "true" ]; then
    apt_auth_flags+=("--allow-unauthenticated")
fi

sudo apt-get install -y "${apt_auth_flags[@]}" archivematica-storage-service

sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/storage /etc/nginx/sites-enabled/storage

sudo apt-get install -y "${apt_auth_flags[@]}" archivematica-mcp-server
if [ "${search_enabled}" != "true" ] ; then
    set_search_env_flags "/etc/default" "false" "mcp-server"
fi

sudo apt-get install -y "${apt_auth_flags[@]}" archivematica-dashboard
if [ "${search_enabled}" != "true" ] ; then
    set_search_env_flags "/etc/default" "false" "dashboard"
fi

sudo apt-get install -y "${apt_auth_flags[@]}" archivematica-mcp-client
if [ "${search_enabled}" != "true" ] ; then
    set_search_env_flags "/etc/default" "false" "mcp-client"
fi

sudo ln -sf /etc/nginx/sites-available/dashboard.conf /etc/nginx/sites-enabled/dashboard.conf

sudo systemctl restart clamav-freshclam
wait_for_service_active "clamav-freshclam" 120 5
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

run_archivematica_manage storage-service collectstatic --noinput --clear
if ! storage_service_code_dir=$(
    first_existing_dir \
        /opt/archivematica/archivematica-storage-service \
        /usr/share/archivematica/storage-service \
        /usr/lib/archivematica/storage-service
); then
    echo "Unable to locate storage service source directory" >&2
    exit 1
fi
run_archivematica_manage storage-service --chdir "${storage_service_code_dir}" compilemessages
