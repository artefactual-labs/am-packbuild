#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -x

THIS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=tests/archivematica/common/helpers.sh
source "${THIS_DIR}/../common/helpers.sh"

wait_for_clamav_databases() {
    local timeout="${1:-120}"
    local interval=2
    local elapsed=0

    until {
        { [ -s /var/lib/clamav/main.cvd ] || [ -s /var/lib/clamav/main.cld ]; } &&
            { [ -s /var/lib/clamav/daily.cvd ] || [ -s /var/lib/clamav/daily.cld ]; }
    }; do
        if [ "${elapsed}" -ge "${timeout}" ]; then
            echo "ClamAV databases were not downloaded within ${timeout}s" >&2
            return 1
        fi
        sleep "${interval}"
        elapsed=$((elapsed + interval))
    done
}

patch_mysql_postinst() {
    local candidate
    local postinst=""
    local matches=0
    local patched_postinst
    local patch_program
    local postinst_candidates=()

    # Keep the AWK variables and the literal $tmpdir for the maintainer script.
    # shellcheck disable=SC2016
    patch_program='
        /^[[:space:]]*stop_server[[:space:]]*\(\)[[:space:]]*\{/ {
            in_stop_server = 1
        }
        in_stop_server &&
            /^[[:space:]]*(\/bin\/)?kill([[:space:]]+--)?[[:space:]]+["]?[$][{]?server_pid[}]?["]?[[:space:]]*$/ {
            match($0, /^[[:space:]]*/)
            indent = substr($0, RSTART, RLENGTH)
            print indent "mysqladmin --no-defaults --socket=\"$tmpdir/mysqld.sock\" -uroot shutdown"
            replacements++
            next
        }
        {
            print
        }
        in_stop_server && /^[[:space:]]*}[[:space:]]*$/ {
            in_stop_server = 0
        }
        END {
            if (replacements != 1) {
                exit 42
            }
        }
    '

    shopt -s nullglob
    postinst_candidates=(/var/lib/dpkg/info/mysql-server-*.postinst)
    shopt -u nullglob

    for candidate in "${postinst_candidates[@]}"; do
        if awk "${patch_program}" "${candidate}" >/dev/null; then
            postinst="${candidate}"
            matches=$((matches + 1))
        fi
    done

    if [ "${matches}" -ne 1 ]; then
        echo "Expected one patchable MySQL post-install script, found ${matches}" >&2
        return 1
    fi

    patched_postinst=$(mktemp)
    if ! awk "${patch_program}" "${postinst}" >"${patched_postinst}"; then
        rm -f "${patched_postinst}"
        echo "Unable to patch MySQL shutdown in ${postinst}" >&2
        return 1
    fi
    sudo -u root install --owner=root --group=root --mode=0755 \
        "${patched_postinst}" "${postinst}"
    rm -f "${patched_postinst}"
}

install_mysql_server() {
    local download_dir
    local mysql_server_deb
    local mysql_server_package
    local mysql_server_debs=()
    local mysql_server_packages=()

    mapfile -t mysql_server_packages < <(
        apt-cache depends --important mysql-server |
            awk '
                $1 == "Depends:" &&
                    $2 ~ /^mysql-server-[0-9]+([.][0-9]+)*$/ {
                    print $2
                }
            '
    )
    if [ "${#mysql_server_packages[@]}" -ne 1 ]; then
        echo "Expected one versioned MySQL server dependency, found" \
            "${#mysql_server_packages[@]}" >&2
        return 1
    fi
    mysql_server_package="${mysql_server_packages[0]}"

    sudo -u root apt-get install -y mysql-common
    download_dir=$(mktemp --directory)
    (
        cd "${download_dir}"
        apt-get download "${mysql_server_package}"
    )
    mapfile -t mysql_server_debs < <(
        find "${download_dir}" -maxdepth 1 -type f \
            -name "${mysql_server_package}_*.deb" -print
    )
    if [ "${#mysql_server_debs[@]}" -ne 1 ]; then
        echo "Expected one downloaded ${mysql_server_package} package, found" \
            "${#mysql_server_debs[@]}" >&2
        return 1
    fi
    mysql_server_deb="${mysql_server_debs[0]}"

    # Ubuntu's MySQL package starts a temporary server during configuration
    # and stops it with kill(1). Rootless Podman denies that signal even to
    # container root. Unpack the dynamically resolved package first so its
    # validated stop_server function can use MySQL's socket-based shutdown.
    sudo -u root dpkg --unpack "${mysql_server_deb}"
    patch_mysql_postinst
    sudo -u root apt-get --fix-broken install -y
    sudo -u root apt-get install -y openjdk-8-jre-headless mysql-server
    sudo -u root rm -rf "${download_dir}"
}

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

export DEBIAN_FRONTEND=noninteractive
sudo debconf-set-selections <<< "postfix postfix/mailname string your.hostname.com"
sudo debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
sudo debconf-set-selections <<< "archivematica-storage-service archivematica-storage-service/dbconfig-install boolean true"
sudo debconf-set-selections <<< "archivematica-storage-service archivematica-storage-service/mysql/app-pass password demo-ss"
sudo debconf-set-selections <<< "archivematica-storage-service archivematica-storage-service/app-password-confirm password demo-ss"
sudo debconf-set-selections <<< "archivematica-mcp-server archivematica-mcp-server/dbconfig-install boolean true"
sudo debconf-set-selections <<< "archivematica-mcp-server archivematica-mcp-server/mysql/app-pass password demo-am"
sudo debconf-set-selections <<< "archivematica-mcp-server archivematica-mcp-server/app-password-confirm password demo-am"

configure_archivematica_apt_repos "${local_repository}" "${packages_repo_version}" "${packages_repo_baseurl}"

if [ "${local_repository}" == "true" ]; then
    sudo apt-get -o Acquire::AllowInsecureRepositories=true update
else
    sudo apt-get update
fi
sudo apt-get -y upgrade

install_mysql_server
sudo systemctl daemon-reload
# The package install has already written the final configuration and started MySQL.
start_service_and_wait mysql
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

start_service_and_wait clamav-freshclam
wait_for_clamav_databases
declare -a SERVICES=(
    "clamav-daemon"
    "gearman-job-server"
    "archivematica-mcp-server"
    "archivematica-mcp-client"
    "archivematica-storage-service"
    "archivematica-dashboard"
    "nginx"
)

for service in "${SERVICES[@]}"; do
    if [ "${search_enabled}" != "true" ] &&
        [[ "${service}" =~ ^archivematica-(dashboard|mcp-server|mcp-client)$ ]]; then
        restart_service_and_wait "${service}"
    else
        start_service_and_wait "${service}"
    fi
done

sudo timeout 120 systemctl reload nginx

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
