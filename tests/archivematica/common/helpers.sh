#!/usr/bin/env bash

ARCHIVEMATICA_SERVICES=(
    archivematica-dashboard
    archivematica-mcp-server
    archivematica-mcp-client
    archivematica-storage-service
)

first_existing_dir() {
    local dir
    for dir in "$@"; do
        if [ -d "${dir}" ]; then
            echo "${dir}"
            return 0
        fi
    done
    return 1
}

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

function stop_archivematica_services() {
    for service in "${ARCHIVEMATICA_SERVICES[@]}"; do
        if ! sudo -u root systemctl stop "${service}"; then
            echo "Warning: could not stop ${service}; continuing" >&2
        fi
    done
}

function restart_archivematica_services() {
    for service in "${ARCHIVEMATICA_SERVICES[@]}"; do
        if ! sudo -u root systemctl restart "${service}"; then
            echo "Warning: could not restart ${service}; continuing" >&2
        fi
    done
}

function dump_lowercase_environment_variables() {
    echo "~~~~~~~~ DEBUG ~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    while read -r line; do echo "$line=${!line}"; done < <(compgen -v | grep -v '[^[:lower:]_]' | grep -v '^_$')
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
}

function configure_archivematica_apt_repos() {
    local local_repository="$1"
    local repo_version="${2:-${ARCHIVEMATICA_PACKAGES_REPO_VERSION:-1.18.x}}"
    local version_slug="${repo_version//\//-}"
    local keyring_path="/etc/apt/keyrings/archivematica-${version_slug}.gpg"

    local arch
    arch=$(dpkg --print-architecture)
    local version_codename
    version_codename=$(grep -Po '(?<=^VERSION_CODENAME=).+' /etc/os-release)

    sudo -u root install -d -m 0755 /etc/apt/keyrings
    curl -fsSL "https://packages.archivematica.org/${repo_version}/key.asc" | sudo -u root gpg --dearmor --yes -o "${keyring_path}"
    sudo -u root bash -c "cat <<EOF > /etc/apt/sources.list.d/archivematica-externals.list
deb [arch=${arch} signed-by=${keyring_path}] http://packages.archivematica.org/${repo_version}/ubuntu-externals jammy main
EOF"

    if [ "${local_repository}" == "true" ]; then
        sudo -u root bash -c "cat << EOF > /etc/apt/sources.list.d/archivematica.list
deb file:/am-packbuild/debs/${version_codename}/_deb_repository ./
EOF"
    else

        sudo -u root bash -c "cat <<EOF > /etc/apt/sources.list.d/archivematica.list
deb [arch=${arch} signed-by=${keyring_path}] http://packages.archivematica.org/${repo_version}/ubuntu ${version_codename} main
EOF"
    fi
}

function configure_archivematica_yum_repos() {
    local local_repository="$1"
    local repo_version="${2:-${ARCHIVEMATICA_PACKAGES_REPO_VERSION:-1.18.x}}"

    if [ "${local_repository}" == "true" ]; then
        sudo -u root bash -c 'cat << EOF > /etc/yum.repos.d/archivematica.repo
[archivematica]
name=archivematica
baseurl=file:///am-packbuild/rpms/EL9/_yum_repository/
enabled=1
gpgcheck=0
EOF'
    else
        sudo -u root bash -c "cat <<EOF > /etc/yum.repos.d/archivematica.repo
[archivematica]
name=archivematica
baseurl=https://packages.archivematica.org/${repo_version}/rocky9
gpgcheck=1
gpgkey=https://packages.archivematica.org/GPG-KEY-archivematica-sha512
enabled=1
EOF"
    fi

    sudo -u root bash -c "cat <<EOF > /etc/yum.repos.d/archivematica-extras.repo
[archivematica-extras]
name=archivematica-extras
baseurl=https://packages.archivematica.org/${repo_version}/rocky9-extras
gpgcheck=1
gpgkey=https://packages.archivematica.org/GPG-KEY-archivematica-sha512
enabled=1
EOF"
}

function set_env_var() {
    local file="$1"
    local variable="$2"
    local value="$3"

    sudo -u root touch "${file}"

    local escaped_variable
    escaped_variable=$(printf '%s' "${variable}" | sed -e 's/[][\\\/.^$*+?|(){}-]/\\&/g')

    if sudo -u root grep -qE "^${escaped_variable}=" "${file}"; then
        sudo -u root sed -i -E "s|^${escaped_variable}=.*|${variable}=${value}|" "${file}"
    else
        echo "${variable}=${value}" | sudo -u root tee -a "${file}" >/dev/null
    fi
}

function ensure_elasticsearch_setting() {
    local key="$1"
    local value="$2"
    local file="${3:-/etc/elasticsearch/elasticsearch.yml}"

    local key_regex
    key_regex=$(printf '%s' "${key}" | sed -e 's/[][\\\/.^$*+?|(){}]/\\&/g')

    local match_regex="^[[:space:]]*${key_regex}:"

    if sudo -u root grep -Eq "${match_regex}" "${file}"; then
        sudo -u root sed -i -E "s|${match_regex}.*|${key}: ${value}|" "${file}"
    else
        printf '%s: %s\n' "${key}" "${value}" | sudo -u root tee -a "${file}" >/dev/null
    fi
}

function configure_elasticsearch_settings() {
    sudo -u root sed -i 's/^xpack\.security\.enabled:.*/xpack.security.enabled: false/' /etc/elasticsearch/elasticsearch.yml
    sudo -u root sed -i '/xpack\.security\.http\.ssl:/,/^xpack\.security/{s/^\(\s*\)enabled:.*/\1enabled: false/}' /etc/elasticsearch/elasticsearch.yml
    sudo -u root sed -i '/xpack\.security\.transport\.ssl:/,/^xpack\.security/{s/^\(\s*\)enabled:.*/\1enabled: false/}' /etc/elasticsearch/elasticsearch.yml
    ensure_elasticsearch_setting "reindex.remote.whitelist" "localhost:9500"
    ensure_elasticsearch_setting "xpack.ml.enabled" "false"
}

function set_search_env_flags() {
    local base_dir="$1"
    local value="$2"
    shift 2

    local components=("$@")
    if [ "${#components[@]}" -eq 0 ]; then
        components=("dashboard" "mcp-server" "mcp-client")
    fi

    for component in "${components[@]}"; do
        case "${component}" in
            dashboard)
                set_env_var "${base_dir}/archivematica-dashboard" "ARCHIVEMATICA_DASHBOARD_DASHBOARD_SEARCH_ENABLED" "${value}"
                ;;
            mcp-server)
                set_env_var "${base_dir}/archivematica-mcp-server" "ARCHIVEMATICA_MCPSERVER_MCPSERVER_SEARCH_ENABLED" "${value}"
                ;;
            mcp-client)
                set_env_var "${base_dir}/archivematica-mcp-client" "ARCHIVEMATICA_MCPCLIENT_MCPCLIENT_SEARCH_ENABLED" "${value}"
                ;;
            *)
                echo "Unknown component '${component}'" >&2
                exit 1
                ;;
        esac
    done
}

function wait_for_elasticsearch() {
    local url="${1:-http://localhost:9200}"
    local timeout="${2:-120}"
    local interval="${3:-5}"
    local elapsed=0

    echo "Waiting for Elasticsearch at ${url} (timeout ${timeout}s)..."
    until curl --silent --fail --max-time 5 "${url}/_cluster/health" >/dev/null; do
        sleep "${interval}"
        elapsed=$((elapsed + interval))
        if [ "${elapsed}" -ge "${timeout}" ]; then
            echo "Elasticsearch at ${url} did not become ready within ${timeout}s" >&2
            return 1
        fi
    done
    echo "Elasticsearch at ${url} is ready."
}

function run_archivematica_manage() {
    local component="$1"
    shift

    local chdir=""
    if [ "$1" == "--chdir" ]; then
        chdir="$2"
        shift 2
    fi

    local env_candidates=()
    local virtualenv_python=""
    local module_candidates=()

    case "${component}" in
        storage-service)
            env_candidates=(
                /etc/default/archivematica-storage-service
                /etc/sysconfig/archivematica-storage-service
            )
            virtualenv_python=/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/python
            module_candidates=(
                archivematica.storage_service.manage
                storage_service.manage
            )
            ;;
        dashboard)
            env_candidates=(
                /etc/default/archivematica-dashboard
                /etc/sysconfig/archivematica-dashboard
            )
            virtualenv_python=/usr/share/archivematica/virtualenvs/archivematica/bin/python
            module_candidates=(
                archivematica.dashboard.manage
                dashboard.manage
            )
            ;;
        *)
            echo "Unknown component '${component}'" >&2
            exit 1
            ;;
    esac

    local env_file=""
    for candidate in "${env_candidates[@]}"; do
        if [ -f "${candidate}" ]; then
            env_file="${candidate}"
            break
        fi
    done

    if [ -z "${env_file}" ]; then
        echo "Environment file not found for component '${component}'" >&2
        exit 1
    fi

    local module=""
    for candidate_module in "${module_candidates[@]}"; do
        if sudo -u archivematica bash -c "set -a -e
source ${env_file}
${virtualenv_python} -c \"import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('${candidate_module}') else 1)\"
" >/dev/null 2>&1; then
            module="${candidate_module}"
            break
        fi
    done

    local command=()
    local activate_path=""
    if [ -n "${module}" ]; then
        command=("${virtualenv_python}" "-m" "${module}" "$@")
        activate_path=$(dirname "${virtualenv_python}")/activate
    else
        # Fall back to manage.py for very old virtualenv layouts lacking modules.
        local manage_py=""
        local manage_candidates=()
        case "${component}" in
            storage-service)
                manage_candidates=(
                    /usr/share/archivematica/storage-service/manage.py
                    /usr/lib/archivematica/storage-service/manage.py
                )
                ;;
            dashboard)
                # Older 1.17.x packages install manage.py under dashboard/.
                manage_candidates=(
                    /usr/share/archivematica/dashboard/manage.py
                    /usr/lib/archivematica/dashboard/manage.py
                )
                ;;
        esac

        for candidate_manage in "${manage_candidates[@]}"; do
            if [ -f "${candidate_manage}" ]; then
                manage_py="${candidate_manage}"
                break
            fi
        done

        if [ ! -f "${manage_py}" ]; then
            echo "Unable to find Python manage module for component '${component}'" >&2
            exit 1
        fi

        local manage_dir
        manage_dir=$(dirname "${manage_py}")
        local default_venv="${manage_dir}/../src/virtualenv/bin/activate"
        if [ ! -f "${default_venv}" ]; then
            default_venv="${manage_dir}/../src/dashboard/virtualenv/bin/activate"
        fi

        command=("${virtualenv_python}" "${manage_py}" "$@")
        activate_path="${default_venv}"
    fi
    local command_string=""
    printf -v command_string '%q ' "${command[@]}"
    command_string=${command_string% }

    local script="set -a -e -x
source ${env_file}
"
    if [ -n "${activate_path}" ] && [ -f "${activate_path}" ]; then
        script+="source ${activate_path}
"
    fi
    if [ -n "${chdir}" ]; then
        script+="cd ${chdir}
"
    fi
    script+="${command_string}
"

    sudo -u archivematica bash -c "${script}"
}

function install_elasticsearch_deb() {
    local repo_version="${1:-${ELASTICSEARCH_PACKAGES_REPO_VERSION:-8.x}}"
    local package_version="${2:-${ELASTICSEARCH_PACKAGE_VERSION:-}}"
    local local_repository="${3:-$(get_env_boolean "LOCAL_REPOSITORY" "false")}"
    local version_slug="${repo_version//\//-}"
    local keyring_path="/etc/apt/keyrings/elasticsearch-${version_slug}.gpg"
    local repo_file="/etc/apt/sources.list.d/elasticsearch-${version_slug}.list"

    sudo -u root install -d -m 0755 /etc/apt/keyrings
    curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo -u root gpg --dearmor --yes -o "${keyring_path}"
    sudo -u root bash -c "cat <<EOF > ${repo_file}
deb [signed-by=${keyring_path}] https://artifacts.elastic.co/packages/${repo_version}/apt stable main
EOF"

    local apt_update_cmd=(sudo -u root apt-get)
    if [ "${local_repository}" == "true" ]; then
        apt_update_cmd+=(-o Acquire::AllowInsecureRepositories=true)
    fi
    apt_update_cmd+=(update)
    "${apt_update_cmd[@]}"
    if [ -n "${package_version}" ]; then
        sudo -u root apt-get install -y "elasticsearch=${package_version}"
    else
        sudo -u root apt-get install -y elasticsearch
    fi

    configure_elasticsearch_settings

    sudo -u root systemctl daemon-reload
    sudo -u root service elasticsearch restart
    sudo -u root systemctl enable elasticsearch

    wait_for_elasticsearch "http://localhost:9200"
}

function install_elasticsearch_rpm() {
    local repo_version="${1:-${ELASTICSEARCH_PACKAGES_REPO_VERSION:-8.x}}"
    local package_version="${2:-${ELASTICSEARCH_PACKAGE_VERSION:-}}"
    local version_slug="${repo_version//\//-}"
    local repo_file="/etc/yum.repos.d/elasticsearch-${version_slug}.repo"

    sudo -u root rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
    sudo -u root bash -c "cat <<EOF > ${repo_file}
[elasticsearch-${version_slug}]
name=Elasticsearch repository for ${repo_version} packages
baseurl=https://artifacts.elastic.co/packages/${repo_version}/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF"

    if [ -n "${package_version}" ]; then
        sudo -u root yum install -y "elasticsearch-${package_version}"
    else
        sudo -u root yum install -y elasticsearch
    fi

    configure_elasticsearch_settings

    sudo -u root systemctl enable elasticsearch
    sudo -u root systemctl start elasticsearch

    wait_for_elasticsearch "http://localhost:9200"
}
