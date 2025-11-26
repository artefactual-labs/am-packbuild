#!/usr/bin/env bash

TEMP_ES6_DIR="/tmp/temp-es-6x"
TEMP_ES6_PID_FILE="${TEMP_ES6_DIR}/elasticsearch-6.8.23/elastic-6x-tmp.pid"

function setup_temp_elasticsearch6() {
    local temp_dir="${TEMP_ES6_DIR}"
    mkdir -p "${temp_dir}"

    local java_bin
    java_bin=$(readlink -f "$(which java)")
    local java_home
    java_home=$(dirname "$(dirname "${java_bin}")")
    echo "Java 11 installed at: ${java_home}"

    (
        cd "${temp_dir}" || exit

        local es_archive="elasticsearch-6.8.23.tar.gz"
        local es_checksum="${es_archive}.sha512"

        rm -f "${es_archive}" "${es_checksum}"
        curl -fSLO "https://artifacts.elastic.co/downloads/elasticsearch/${es_archive}"
        curl -fSLO "https://artifacts.elastic.co/downloads/elasticsearch/${es_checksum}"

        if ! sha512sum --check --status "${es_checksum}"; then
            echo "Failed to verify checksum for ${es_archive}" >&2
            exit 1
        fi
        rm -f "${es_checksum}"

        rm -rf elasticsearch-6.8.23
        tar --extract --gzip --verbose --file "${es_archive}"

        (
            cd elasticsearch-6.8.23 || exit
            sudo -u root rm -rf data
            sudo -u root cp /var/lib/elasticsearch data --recursive --force
            sudo -u root chown "$(whoami)":"$(whoami)" data --recursive
            JAVA_HOME="${java_home}" ES_JAVA_OPTS="-Xms2g -Xmx2g" ./bin/elasticsearch \
                --daemonize --pidfile elastic-6x-tmp.pid \
                -Ehttp.port=9500 \
                -Ediscovery.type=single-node
        )
    ) || return 1

    wait_for_elasticsearch "http://localhost:9500"
    curl --request GET "localhost:9500/_cat/indices?v"
}

function cleanup_temp_elasticsearch6() {
    local pid_file="${TEMP_ES6_PID_FILE}"

    if [ -f "${pid_file}" ]; then
        local pid
        pid=$(cat "${pid_file}")
        if [ -n "${pid}" ] && kill -0 "${pid}" 2>/dev/null; then
            kill "${pid}" || true
        fi
        rm -f "${pid_file}"
    fi

    sudo -u root rm -rf "${TEMP_ES6_DIR}/elasticsearch-6.8.23"
    rm -f "${TEMP_ES6_DIR}/elasticsearch-6.8.23.tar.gz"
}

function reindex_elasticsearch_data() {
    local indices=("aips" "aipfiles" "transfers" "transferfiles")

    wait_for_elasticsearch "http://localhost:9200"

    for index in "${indices[@]}"; do
        curl --request POST "localhost:9200/_reindex?pretty" \
            --header 'Content-Type: application/json' \
            --data @- <<EOF
{
  "source": {
    "remote": {
      "host": "http://localhost:9500"
    },
    "index": "${index}"
  },
  "dest": {
    "index": "${index}"
  }
}
EOF
    done

    curl -X POST "http://localhost:9200/_flush"
    curl --request GET "localhost:9200/_cat/indices?v"
}
