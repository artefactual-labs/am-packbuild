#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE}")/../../" && pwd)"

build_local_repository="false"
if [ "${LOCAL_REPOSITORY}" = "yes" ] || [ "${LOCAL_REPOSITORY}" = "true" ] || [ "${LOCAL_REPOSITORY}" = "1" ]; then
    build_local_repository="true"
fi

function add_remote_apt_key() {
    sudo curl -s ${1} | sudo apt-key add -
}

function start_service() {
    sudo systemctl -q enable $1
    if $(sudo systemctl -q is-active $1) ; then
        sudo systemctl -q start $1
    fi
}

function create_local_repository() {
    local src="${ROOT}/debs/xenial"
    local repo="${1}"

    # Install dpkg-dev
    sudo apt-get install --yes dpkg-dev

    # Copy debs
    mkdir -p ${repo} || true
    find ${src}/{archivematica/repo,archivematica-storage-service/repo} -name '*.deb' | xargs -IF cp F ${repo}
    cd ${repo}

    # Generate files Packages and Release
    dpkg-scanpackages . /dev/null > Packages
    gzip --keep --force -9 Packages
    cat << EOF > Release
Origin: My_Local_Repo
Label: My_Local_Repo
Codename: xenial
Architectures: amd64
Components: main
Description: My local APT repository
EOF
    echo -e "Date: `LANG=C date -Ru`" >> Release
    echo -e 'MD5Sum:' >> Release
    printf ' '$(md5sum Packages.gz | cut --delimiter=' ' --fields=1)' %16d Packages.gz' $(wc --bytes Packages.gz | cut --delimiter=' ' --fields=1) >> Release
    printf '\n '$(md5sum Packages | cut --delimiter=' ' --fields=1)' %16d Packages' $(wc --bytes Packages | cut --delimiter=' ' --fields=1) >> Release
    echo -e '\nSHA256:' >> Release
    printf ' '$(sha256sum Packages.gz | cut --delimiter=' ' --fields=1)' %16d Packages.gz' $(wc --bytes Packages.gz | cut --delimiter=' ' --fields=1) >> Release
    printf '\n '$(sha256sum Packages | cut --delimiter=' ' --fields=1)' %16d Packages' $(wc --bytes Packages | cut --delimiter=' ' --fields=1) >> Release

    # Sign it using our dummy keys
    chmod 700 ${ROOT}/deb-testing/.gnupg
    chmod 600 ${ROOT}/deb-testing/.gnupg/*
    sudo apt-key add ${ROOT}/deb-testing/.gnupg/pubring.gpg
    gpg --batch --yes --clearsign --digest-algo SHA512 --homedir ${ROOT}/deb-testing/.gnupg -o InRelease Release
}

readonly remote_apt_keys=(
    "https://packages.archivematica.org/1.7.x/key.asc"
    "http://jenkins-ci.archivematica.org/repos/devel.key"
    "https://packages.elasticsearch.org/GPG-KEY-elasticsearch"
)

apt_repositories=(
    "deb [arch=amd64] http://packages.archivematica.org/1.7.x/ubuntu-externals xenial main"
    "deb http://packages.elasticsearch.org/elasticsearch/1.7/debian stable main"
)

readonly packages=(
    "elasticsearch"
    "archivematica-storage-service"
    "archivematica-mcp-server"
    "archivematica-dashboard"
    "archivematica-mcp-client"
)

readonly services=(
    "elasticsearch"
    "clamav-freshclam"
    "clamav-daemon"
    "fits"
    "nginx"
    "gearman-job-server"
    "archivematica-mcp-server"
    "archivematica-mcp-client"
    "archivematica-storage-service"
    "archivematica-dashboard"
)

sudo apt-get update
sudo apt-get upgrade --yes
sudo apt-get install --yes python

if [ "${build_local_repository}" == "true" ] ; then
    repo="${ROOT}/deb-testing/.repo"
    create_local_repository "${repo}"
    apt_repositories+=("deb file:${repo} ./")
else
    apt_repositories+=("deb http://jenkins-ci.archivematica.org/repos/apt/release-0.11-xenial/ ./")
    apt_repositories+=("deb http://jenkins-ci.archivematica.org/repos/apt/release-1.7-xenial/ ./")
fi

for item in "${remote_apt_keys[@]}"; do
    add_remote_apt_key "${item}"
done

for item in "${apt_repositories[@]}"; do
    add-apt-repository "${item}"
done

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password your_password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password your_password'
sudo debconf-set-selections <<< "postfix postfix/mailname string your.hostname.com"
sudo debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
sudo debconf-set-selections <<< "archivematica-mcp-server archivematica-mcp-server/dbconfig-install boolean true"

curl -s https://bootstrap.pypa.io/get-pip.py | sudo python -
sudo apt-get update
for item in "${packages[@]}"; do
    sudo DEBIAN_FRONTEND=noninteractive apt-get install --yes ${item}
done

sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/storage /etc/nginx/sites-enabled/storage
sudo ln -sf /etc/nginx/sites-available/dashboard.conf /etc/nginx/sites-enabled/dashboard.conf
sudo systemctl reload nginx

for item in "${services[@]}"; do
    start_service "${item}"
done
