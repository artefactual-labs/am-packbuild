#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -x

THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=tests/archivematica/common/helpers.sh
source "${THIS_DIR}/../common/helpers.sh"
# shellcheck source=tests/archivematica/common/elasticsearch.sh
source "${THIS_DIR}/../common/elasticsearch.sh"

trap cleanup_temp_elasticsearch6 EXIT

local_repository=$(get_env_boolean "LOCAL_REPOSITORY" "false")
packages_repo_version="${ARCHIVEMATICA_PACKAGES_REPO_VERSION:-1.18.x}"
packages_repo_baseurl="${ARCHIVEMATICA_PACKAGES_REPO_BASEURL:-}"
elasticsearch_repo_version="${ELASTICSEARCH_PACKAGES_REPO_VERSION:-8.x}"
elasticsearch_package_version="${ELASTICSEARCH_PACKAGE_VERSION:-}"
elasticsearch_migrate_from_6x=$(get_env_boolean "ELASTICSEARCH_MIGRATE_FROM_6X" "true")

dump_lowercase_environment_variables
echo "Using Archivematica packages repository version: ${packages_repo_version}"
if [ -n "${packages_repo_baseurl}" ]; then
    echo "Using Archivematica packages repository base URL: ${packages_repo_baseurl}"
fi
echo "Using Elasticsearch packages repository version: ${elasticsearch_repo_version}"
if [ -n "${elasticsearch_package_version}" ]; then
    echo "Using Elasticsearch package version: ${elasticsearch_package_version}"
fi
echo "Elasticsearch 6.x migration enabled: ${elasticsearch_migrate_from_6x}"

# Stop Archivematica services.
stop_archivematica_services

if [ "${elasticsearch_migrate_from_6x}" == "true" ]; then
    # Back up Elasticsearch data.
    sudo -u root systemctl stop elasticsearch
    sudo -u root tar --create --gzip --file "/root/var_lib_elasticsearch_$(date +%y%m%d).tgz" /var/lib/elasticsearch

    # Set up temporary Elasticsearch 6.x instance.
    if [ "${local_repository}" == "true" ]; then
        sudo -u root apt-get -o Acquire::AllowInsecureRepositories=true update
    else
        sudo -u root apt-get update
    fi
    sudo -u root apt-get install -y openjdk-11-jdk gnupg

    # Set up Elasticsearch 6.x.
    setup_temp_elasticsearch6

    # Back up Elasticsearch 6.x directories.
    sudo -u root cp -a /etc/elasticsearch /etc/elasticsearch-6
    sudo -u root cp -a /var/lib/elasticsearch /var/lib/elasticsearch-6
    sudo -u root cp -a /var/log/elasticsearch /var/log/elasticsearch-6

    # Remove Elasticsearch 6.x.
    sudo -u root apt-get purge -y elasticsearch
    sudo -u root rm -rf /var/lib/elasticsearch /var/log/elasticsearch /etc/elasticsearch
fi

# Install/upgrade Elasticsearch 8.x.
install_elasticsearch_deb "${elasticsearch_repo_version}" "${elasticsearch_package_version}" "${local_repository}"

sudo -u root systemctl restart elasticsearch
wait_for_elasticsearch "http://localhost:9200"

#
# Configure repository
#

configure_archivematica_apt_repos "${local_repository}" "${packages_repo_version}" "${packages_repo_baseurl}"

if [ "${local_repository}" == "true" ]; then
    sudo -u root apt-get -o Acquire::AllowInsecureRepositories=true update
else
    sudo -u root apt-get update
fi

apt_upgrade_cmd=(
    sudo -u root apt-get install -y
    -o Dpkg::Options::="--force-confnew"
    -o Dpkg::Options::="--force-confmiss"
)
if [ "${local_repository}" == "true" ]; then
    apt_upgrade_cmd+=("--allow-unauthenticated")
fi
apt_upgrade_cmd+=(
    archivematica-storage-service
)
"${apt_upgrade_cmd[@]}"

apt_upgrade_cmd=(
    sudo -u root apt-get install -y
    -o Dpkg::Options::="--force-confnew"
    -o Dpkg::Options::="--force-confmiss"
)
if [ "${local_repository}" == "true" ]; then
    apt_upgrade_cmd+=("--allow-unauthenticated")
fi
apt_upgrade_cmd+=(
    archivematica
    archivematica-common
)
"${apt_upgrade_cmd[@]}"

apt_upgrade_cmd=(
    sudo -u root apt-get install -y
    -o Dpkg::Options::="--force-confnew"
    -o Dpkg::Options::="--force-confmiss"
)
if [ "${local_repository}" == "true" ]; then
    apt_upgrade_cmd+=("--allow-unauthenticated")
fi
apt_upgrade_cmd+=(
    archivematica-dashboard
    archivematica-mcp-server
    archivematica-mcp-client
)

"${apt_upgrade_cmd[@]}"

restart_archivematica_services

if [ "${elasticsearch_migrate_from_6x}" == "true" ]; then
    # Reindex Elasticsearch data (only needed when migrating from 6.x).
    reindex_elasticsearch_data

    # Delete temporary Elasticsearch 6.x instance.
    cleanup_temp_elasticsearch6
    trap - EXIT
fi
