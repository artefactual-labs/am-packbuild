%global __brp_python_bytecompile %{nil}
%global __brp_mangle_shebangs %{nil}

#
# Packages
#

Name: archivematica
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Archivematica digital preservation system
Group: Application/System
License: AGPLv3
Source0: %{git_repo}
BuildRequires: git, gcc, openldap-devel, openssl-devel, python3-virtualenv, mariadb-devel, libxslt-devel, python3.12-devel, libffi-devel, gcc-c++, postgresql-devel, nodejs >= 24, pkgconfig
Requires: python3.12-devel
AutoReq: No
AutoProv: No
%description
Archivematica is a web- and standards-based, open-source application which allows your institution to preserve long-term access to trustworthy, authentic and reliable digital content.

%package common
Summary: Archivematica common libraries
Requires: archivematica, shadow-utils
%description common
Common files and libraries for Archivematica.

%package mcp-server
Requires: archivematica, archivematica-common
Summary: Archivematica MCP server
AutoReq: No
AutoProv: No

%description mcp-server
Archivematica MCP server.

%package mcp-client
Summary: Archivematica MCP client
Requires: archivematica, archivematica-common
Requires: bzip2
Requires: tesseract
Requires: tree
Requires: p7zip
Requires: p7zip-plugins
Requires: pbzip2
Requires: ImageMagick
Requires: ghostscript
Requires: perl-Image-ExifTool
Requires: inkscape
Requires: clamav-data
Requires: clamav-update
Requires: clamav-filesystem
Requires: clamav
Requires: clamav-devel
Requires: clamav-lib
Requires: clamd
Requires: libvpx
Requires: libraw1394
Requires: libpst
Requires: openjpeg2
Requires: mediainfo
Requires: mediaconch
Requires: md5deep
Requires: uuid
# Packages from Archivematica repo
Requires: siegfried
Requires: atool
Requires: jhove
# Packages from https://forensics.cert.org/
Requires: bulk_extractor
Requires: sleuthkit
Requires: libewf
# Packages from Nux repo
Requires: ffmpeg

AutoReq: No
AutoProv: No
%description mcp-client
Archivematica MCP client.

%package dashboard
Summary: Archivematica dashboard
Requires: archivematica, nginx, policycoreutils-python-utils, gettext
AutoReq: No
AutoProv: No
%description dashboard
Archivematica dashboard with Nginx + gunicorn.

#
# Files
#

# Archivematica
%files
/usr/share/archivematica/virtualenvs/archivematica/
/opt/archivematica/archivematica/

# Common
%files common
/var/archivematica/sharedDirectory/

# MCPServer
%files mcp-server
/usr/lib/systemd/system/archivematica-mcp-server.service
%config(noreplace) /etc/sysconfig/archivematica-mcp-server
%config(noreplace) /etc/archivematica/serverConfig.conf
%config(noreplace) /etc/archivematica/serverConfig.logging.json

# MCPClient
%files mcp-client
/usr/lib/systemd/system/archivematica-mcp-client.service
%config(noreplace) /etc/sysconfig/archivematica-mcp-client
%config(noreplace) /etc/archivematica/clientConfig.conf
%config(noreplace) /etc/archivematica/clientConfig.logging.json

# Dashboard
%files dashboard
/usr/lib/systemd/system/archivematica-dashboard.service
%config(noreplace) /etc/sysconfig/archivematica-dashboard
%config(noreplace) /etc/nginx/conf.d/archivematica-dashboard.conf
%config(noreplace) /etc/archivematica/dashboard.gunicorn-config.py
%config(noreplace) /etc/archivematica/dashboard.logging.json

#
# Preparations
#

%prep
rm -rf /usr/share/python/archivematica*
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone \
  --quiet \
  --branch %{_branch} \
  --depth 1 \
  --single-branch \
    %{git_repo} \
    %{_sourcedir}/%{name}

# This prevents build conflicts with Python packages that provide shared
# object (*.so) files and are common to AM and SS, for example lxml.
%define _build_id_links none

#
# Install
#

%install
mkdir -p \
  %{buildroot}/etc/archivematica/ \
  %{buildroot}/usr/share/archivematica/virtualenvs/archivematica \
  %{buildroot}/opt/archivematica/archivematica/src/archivematica/dashboard/frontend/dist/ \
  %{buildroot}/var/archivematica/sharedDirectory \
  %{buildroot}/etc/sysconfig \
  %{buildroot}/usr/lib/systemd/system \
  %{buildroot}/etc/nginx/conf.d

# Create runtime source directory under /opt and make the same path available in
# the buildroot. This path is used for editable install.
mkdir -p /opt/archivematica/archivematica
cp -a %{_sourcedir}/%{name}/. /opt/archivematica/archivematica/
cp -a %{_sourcedir}/%{name}/. %{buildroot}/opt/archivematica/archivematica/

# Archivematica virtual environment
virtualenv --python=python3.12 /usr/share/archivematica/virtualenvs/archivematica
/usr/share/archivematica/virtualenvs/archivematica/bin/pip install --upgrade pip setuptools
UV_PYTHON=python3.12 UV_PYTHON_DOWNLOADS=never \
  uv export --project %{_sourcedir}/%{name} --locked --no-dev --no-hashes \
    --no-emit-project --output-file %{_builddir}/uv-runtime-requirements.txt
/usr/share/archivematica/virtualenvs/archivematica/bin/pip install -r %{_builddir}/uv-runtime-requirements.txt

# Install the application in editable mode so the source directory under /opt is
# importable by the virtualenv at runtime.
/usr/share/archivematica/virtualenvs/archivematica/bin/pip install --no-deps --editable /opt/archivematica/archivematica
cp -rf /usr/share/archivematica/virtualenvs/archivematica/* %{buildroot}/usr/share/archivematica/virtualenvs/archivematica/

# MCPServer
cp %{_sourcedir}/%{name}/src/archivematica/MCPServer/install/serverConfig.logging.json %{buildroot}/etc/archivematica/serverConfig.logging.json
cp %{_sourcedir}/%{name}/src/archivematica/MCPServer/install/serverConfig.conf %{buildroot}/etc/archivematica/serverConfig.conf
cp %{_etcdir}/archivematica-mcp-server.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-server.service
cp %{_etcdir}/archivematica-mcp-server.env %{buildroot}/etc/sysconfig/archivematica-mcp-server

# MCPClient
cp %{_sourcedir}/%{name}/src/archivematica/MCPClient/install/clientConfig.logging.json %{buildroot}/etc/archivematica/clientConfig.logging.json
cp %{_sourcedir}/%{name}/src/archivematica/MCPClient/install/clientConfig.conf %{buildroot}/etc/archivematica/clientConfig.conf
cp %{_etcdir}/archivematica-mcp-client.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-client.service
cp %{_etcdir}/archivematica-mcp-client.env %{buildroot}/etc/sysconfig/archivematica-mcp-client

# Dashboard
cp %{_sourcedir}/%{name}/src/archivematica/dashboard/install/dashboard.gunicorn-config.py %{buildroot}/etc/archivematica/dashboard.gunicorn-config.py
cp %{_sourcedir}/%{name}/src/archivematica/dashboard/install/dashboard.logging.json %{buildroot}/etc/archivematica/dashboard.logging.json
cp %{_etcdir}/archivematica-dashboard.service %{buildroot}/usr/lib/systemd/system/archivematica-dashboard.service
cp %{_etcdir}/archivematica-dashboard.env %{buildroot}/etc/sysconfig/archivematica-dashboard
cp %{_etcdir}/dashboard.nginx %{buildroot}/etc/nginx/conf.d/archivematica-dashboard.conf

cd %{_sourcedir}/%{name}/src/archivematica/dashboard/frontend/ && npm clean-install --unsafe-perm
cd %{_sourcedir}/%{name}/src/archivematica/dashboard/frontend/ && npm run build
test -d %{_sourcedir}/%{name}/src/archivematica/dashboard/frontend/dist
cp -a %{_sourcedir}/%{name}/src/archivematica/dashboard/frontend/dist/. %{buildroot}/opt/archivematica/archivematica/src/archivematica/dashboard/frontend/dist/

#
# Clean up build directory
#

%clean
rm -rf %{buildroot}

#
# Post install scripts
#

%post common

# Create archivematica user and group
getent group archivematica >/dev/null || groupadd -f -g 333 -r archivematica
if ! getent passwd archivematica >/dev/null ; then
  if ! getent passwd 333 >/dev/null ; then
    useradd -r -u 333 -g archivematica -d /var/lib/archivematica/ -s /sbin/nologin -c "Archivematica system account" -m archivematica
    else
    useradd -r -g archivematica -d /var/lib/archivematica/ -s /sbin/nologin -c "Archivematica system account" -m archivematica
  fi
fi

# Configure permissions of shared directory
chown -R archivematica:archivematica /var/archivematica/sharedDirectory

# MCPServer
%post mcp-server
mkdir -p /var/log/archivematica/MCPServer
chown -R archivematica:archivematica /var/log/archivematica/MCPServer
systemctl daemon-reload

# MCPClient
%post mcp-client
mkdir -p /var/log/archivematica/MCPClient
chown -R archivematica:archivematica /var/log/archivematica/MCPClient
systemctl daemon-reload

# Dashboard
%post dashboard
mkdir -p /var/log/archivematica/dashboard

# Create Django key
KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
sed -i "s/CHANGE_ME_WITH_A_SECRET_KEY/\"$KEY\"/g" /etc/sysconfig/archivematica-dashboard
# Update SELinux policy
if [ x$(semanage port -l | grep http_port_t | grep 7400 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 7400
fi


#
# Posttrans install script
#

%posttrans mcp-server
if [ -f /etc/sysconfig/archivematica-mcp-server ]; then
  if grep -Eq '^DJANGO_SETTINGS_MODULE="?settings.common"?$' /etc/sysconfig/archivematica-mcp-server; then
    sed -i 's#^DJANGO_SETTINGS_MODULE=.*#DJANGO_SETTINGS_MODULE=archivematica.MCPServer.settings.common#' /etc/sysconfig/archivematica-mcp-server
  fi
  if grep -Eq '^PYTHONPATH="?/usr/lib/archivematica/archivematicaCommon/:/usr/share/archivematica/dashboard/"?$' /etc/sysconfig/archivematica-mcp-server; then
    sed -i -E '/^PYTHONPATH="?\/usr\/lib\/archivematica\/archivematicaCommon\/:\/usr\/share\/archivematica\/dashboard\/"?$/d' /etc/sysconfig/archivematica-mcp-server
  fi
fi

%posttrans mcp-client
if [ -f /etc/sysconfig/archivematica-mcp-client ]; then
  if grep -Eq '^DJANGO_SETTINGS_MODULE="?settings.common"?$' /etc/sysconfig/archivematica-mcp-client; then
    sed -i 's#^DJANGO_SETTINGS_MODULE=.*#DJANGO_SETTINGS_MODULE=archivematica.MCPClient.settings.common#' /etc/sysconfig/archivematica-mcp-client
  fi
  if grep -Eq '^PYTHONPATH="?/usr/lib/archivematica/MCPClient:/usr/lib/archivematica/MCPClient/clientScripts:/usr/lib/archivematica/archivematicaCommon/:/usr/share/archivematica/dashboard/"?$' /etc/sysconfig/archivematica-mcp-client; then
    sed -i -E '/^PYTHONPATH="?\/usr\/lib\/archivematica\/MCPClient:\/usr\/lib\/archivematica\/MCPClient\/clientScripts:\/usr\/lib\/archivematica\/archivematicaCommon\/:\/usr\/share\/archivematica\/dashboard\/"?$/d' /etc/sysconfig/archivematica-mcp-client
  fi
  if grep -Eq '^ARCHIVEMATICA_MCPCLIENT_MCPCLIENT_ELASTICSEARCHSERVER="?localhost:9200"?$' /etc/sysconfig/archivematica-mcp-client; then
    sed -i 's#^ARCHIVEMATICA_MCPCLIENT_MCPCLIENT_ELASTICSEARCHSERVER=.*#ARCHIVEMATICA_MCPCLIENT_MCPCLIENT_ELASTICSEARCHSERVER=http://localhost:9200#' /etc/sysconfig/archivematica-mcp-client
  fi
fi

%posttrans dashboard
if [ -f /etc/sysconfig/archivematica-dashboard ]; then
  if grep -Eq '^DJANGO_SETTINGS_MODULE="?settings.production"?$' /etc/sysconfig/archivematica-dashboard; then
    sed -i 's#^DJANGO_SETTINGS_MODULE=.*#DJANGO_SETTINGS_MODULE=archivematica.dashboard.settings.production#' /etc/sysconfig/archivematica-dashboard
  fi
  if grep -Eq '^PYTHONPATH="?/usr/lib/archivematica/archivematicaCommon/:/usr/share/archivematica/dashboard"?$' /etc/sysconfig/archivematica-dashboard; then
    sed -i -E '/^PYTHONPATH="?\/usr\/lib\/archivematica\/archivematicaCommon\/:\/usr\/share\/archivematica\/dashboard"?$/d' /etc/sysconfig/archivematica-dashboard
  fi
  if grep -Eq '^ARCHIVEMATICA_DASHBOARD_DASHBOARD_ELASTICSEARCH_SERVER="?localhost:9200"?$' /etc/sysconfig/archivematica-dashboard; then
    sed -i 's#^ARCHIVEMATICA_DASHBOARD_DASHBOARD_ELASTICSEARCH_SERVER=.*#ARCHIVEMATICA_DASHBOARD_DASHBOARD_ELASTICSEARCH_SERVER=http://localhost:9200#' /etc/sysconfig/archivematica-dashboard
  fi
  if ! grep -q '^DJANGO_STATIC_ROOT=' /etc/sysconfig/archivematica-dashboard; then
    echo 'DJANGO_STATIC_ROOT=/opt/archivematica/archivematica/src/archivematica/dashboard/static' >> /etc/sysconfig/archivematica-dashboard
  fi
fi
# Update old virtual environment paths in configuration files
sed -i "s/\/usr\/share\/archivematica\/virtualenvs\/archivematica-\(dashboard\|mcp-server\|mcp-client\)\//\/usr\/share\/archivematica\/virtualenvs\/archivematica\//g" \
  /etc/sysconfig/archivematica-mcp-server \
  /etc/sysconfig/archivematica-mcp-client \
  /etc/sysconfig/archivematica-dashboard \
  /usr/lib/systemd/system/archivematica-mcp-server.service \
  /usr/lib/systemd/system/archivematica-mcp-client.service \
  /usr/lib/systemd/system/archivematica-dashboard.service
systemctl daemon-reload
# Run django collectstatic and compilemessages.
# These tasks need to be run after postun script on upgrades
# because the old virtualenv files need to be removed from the old package.
# https://github.com/archivematica/Issues/issues/1312
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#ordering
mkdir -p /opt/archivematica/archivematica/src/archivematica/dashboard/static
bash -c " \
  set -a -e -x
  source /etc/sysconfig/archivematica-dashboard \
    || (echo 'Environment file not found'; exit 1)
  cd /opt/archivematica/archivematica/
  /usr/share/archivematica/virtualenvs/archivematica/bin/python -m archivematica.dashboard.manage collectstatic --noinput --clear
  /usr/share/archivematica/virtualenvs/archivematica/bin/python -m archivematica.dashboard.manage compilemessages
";
chown -R archivematica:archivematica /var/log/archivematica/dashboard
chown -R archivematica:archivematica /opt/archivematica/archivematica/src/archivematica/dashboard/static
chown -R archivematica:archivematica /opt/archivematica/archivematica/src/archivematica/dashboard/locale
systemctl daemon-reload
