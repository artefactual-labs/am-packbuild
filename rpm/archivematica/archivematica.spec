%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


#
# Packages
#

Name: archivematica
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Archivematica digital preservation system
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica
BuildRequires: git, gcc, openldap-devel, openssl-devel, python-virtualenv, python-pip, mariadb-devel, libxslt-devel, python-devel, libffi-devel, openssl-devel, gcc-c++, postgresql-devel, nodejs
Requires: archivematica-common
AutoReq: No
AutoProv: No
%description
Archivematica is a web- and standards-based, open-source application which allows your institution to preserve long-term access to trustworthy, authentic and reliable digital content.

%package common
Summary: Archivematica common libraries
%description common
Common files and libraries for Archivematica.

%package mcp-server
Requires: archivematica-common
Summary: Archivematica MCP server
%description mcp-server
Archivematica MCP server.

%package mcp-client
Summary: Archivematica MCP client
Requires: archivematica-common
Requires: sudo
Requires: tesseract
Requires: p7zip
Requires: ImageMagick
Requires: ghostscript
Requires: perl-Image-ExifTool
Requires: inkscape
Requires: clamav-server
Requires: clamav-data
Requires: clamav-update
Requires: clamav-filesystem
Requires: clamav
Requires: clamav-scanner-systemd
Requires: clamav-devel
Requires: clamav-lib
Requires: clamav-server-systemd
Requires: fido
Requires: libvpx
Requires: libraw1394
Requires: python-unidecode
Requires: libpst
Requires: openjpeg
Requires: mediainfo
# Packages from Archivematica repo
Requires: siegfried
Requires: fits
Requires: bagit-java
Requires: atool
Requires: jhove
# Packages from https://forensics.cert.org/
Requires: bulk_extractor
Requires: sleuthkit
Requires: libewf
# Packages from Nux repo
Requires: ffmpeg
Requires: ufraw

AutoReq: No
AutoProv: No
%description mcp-client
Archivematica MCP client.

%package dashboard
Summary: Archivematica dashboard
Requires: nginx, policycoreutils-python
%description dashboard
Archivematica dashboard with Nginx + gunicorn.


#
# Files
#

# There is no need for a main package "archivematica", so we avoid using the
# unnamed $files tag in this section.

# Common
%files common
/usr/lib/archivematica/archivematicaCommon/
/var/archivematica/sharedDirectory/

# MCPServer
%files mcp-server
/usr/share/python/archivematica-mcp-server/
/usr/lib/archivematica/MCPServer/
/usr/lib/systemd/system/archivematica-mcp-server.service
%config /etc/sysconfig/archivematica-mcp-server

# MCPClient
%files mcp-client
/usr/share/python/archivematica-mcp-client/
/usr/lib/archivematica/MCPClient/
/usr/lib/systemd/system/archivematica-mcp-client.service
%config /etc/sysconfig/archivematica-mcp-client

# Dashboard
%files dashboard
/usr/share/python/archivematica-dashboard/
/usr/share/archivematica/dashboard/
/usr/lib/systemd/system/archivematica-dashboard.service
%config /etc/sysconfig/archivematica-dashboard
%config /etc/nginx/conf.d/archivematica-dashboard.conf
%config /etc/archivematica/dashboard.gunicorn-config.py

#
# Preparations
#

%prep
rm -rf /usr/share/archivematica
rm -rf /usr/lib/archivematica
rm -rf /usr/share/python/archivematica
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone \
  --quiet \
  --branch qa/1.x \
  --depth 1 \
  --single-branch \
  --recurse-submodules \
    https://github.com/artefactual/archivematica \
    %{_sourcedir}/%{name}


#
# Install
#

%install
mkdir -p \
  %{buildroot}/etc/archivematica/ \
  %{buildroot}/usr/lib/archivematica/MCPServer \
  %{buildroot}/usr/lib/archivematica/MCPClient \
  %{buildroot}/usr/lib/archivematica/archivematicaCommon \
  %{buildroot}/usr/share/python/archivematica-mcp-server \
  %{buildroot}/usr/share/python/archivematica-mcp-client \
  %{buildroot}/usr/share/python/archivematica-dashboard \
  %{buildroot}/usr/share/archivematica/dashboard \
  %{buildroot}/var/archivematica/sharedDirectory \
  %{buildroot}/etc/sysconfig \
  %{buildroot}/usr/lib/systemd/system \
  %{buildroot}/etc/nginx/conf.d

# Common
cp -rf %{_sourcedir}/%{name}/src/archivematicaCommon/lib/* %{buildroot}/usr/lib/archivematica/archivematicaCommon/

# MCPServer
virtualenv /usr/share/python/archivematica-mcp-server
/usr/share/python/archivematica-mcp-server/bin/pip install --upgrade pip
/usr/share/python/archivematica-mcp-server/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/share/python/archivematica-mcp-server/bin/pip install -r %{_sourcedir}/%{name}/src/MCPServer/requirements/production.txt
/usr/share/python/archivematica-mcp-server/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
virtualenv --relocatable /usr/share/python/archivematica-mcp-server
cp -rf /usr/share/python/archivematica-mcp-server/* %{buildroot}/usr/share/python/archivematica-mcp-server/
cp -rf %{_sourcedir}/%{name}/src/MCPServer/lib/* %{buildroot}/usr/lib/archivematica/MCPServer/
cp %{_etcdir}/archivematica-mcp-server.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-server.service
cp %{_etcdir}/archivematica-mcp-server.env %{buildroot}/etc/sysconfig/archivematica-mcp-server

# MCPClient
virtualenv /usr/share/python/archivematica-mcp-client
/usr/share/python/archivematica-mcp-client/bin/pip install --upgrade pip
/usr/share/python/archivematica-mcp-client/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/share/python/archivematica-mcp-client/bin/pip install -r %{_sourcedir}/%{name}/src/MCPClient/requirements/production.txt
/usr/share/python/archivematica-mcp-client/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
virtualenv --relocatable /usr/share/python/archivematica-mcp-client
cp -rf /usr/share/python/archivematica-mcp-client/* %{buildroot}/usr/share/python/archivematica-mcp-client/

cp -rf %{_sourcedir}/%{name}/src/MCPClient/lib/* %{buildroot}/usr/lib/archivematica/MCPClient
cp %{_etcdir}/archivematica-mcp-client.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-client.service
cp %{_etcdir}/archivematica-mcp-client.env %{buildroot}/etc/sysconfig/archivematica-mcp-client

# Dashboard
virtualenv /usr/share/python/archivematica-dashboard
/usr/share/python/archivematica-dashboard/bin/pip install --upgrade pip
/usr/share/python/archivematica-dashboard/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/share/python/archivematica-dashboard/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
virtualenv --relocatable /usr/share/python/archivematica-dashboard
cd %{_sourcedir}/%{name}/src/dashboard/frontend/transfer-browser/ && npm install --unsafe-perm 

cd %{_sourcedir}/%{name}/src/dashboard/frontend/appraisal-tab/ && npm install --unsafe-perm

find %{_sourcedir}/%{name}/src/dashboard/ | grep static
cp -rf /usr/share/python/archivematica-dashboard/* %{buildroot}/usr/share/python/archivematica-dashboard/

cp -rf %{_sourcedir}/%{name}/src/dashboard/src/* %{buildroot}/usr/share/archivematica/dashboard/
cp %{_sourcedir}/%{name}/src/dashboard/install/dashboard.gunicorn-config.py %{buildroot}/etc/archivematica/dashboard.gunicorn-config.py
cp %{_etcdir}/archivematica-dashboard.service %{buildroot}/usr/lib/systemd/system/archivematica-dashboard.service
cp %{_etcdir}/archivematica-dashboard.env %{buildroot}/etc/sysconfig/archivematica-dashboard
cp %{_etcdir}/dashboard.nginx %{buildroot}/etc/nginx/conf.d/archivematica-dashboard.conf


#
# Clean up build directory
#

%clean
rm -rf %{buildroot}


#
# Post install scripts
#

# Common
%post common

# Create archivematica user
userID=`id -u archivematica`
if [ "${userID}" != 333 ]; then
  useradd --uid 333 --user-group --home /var/lib/archivematica/ archivematica
fi

# Configure permissions of shared directory
chown -R archivematica:archivematica /var/archivematica/sharedDirectory

# Configure sudoers and check validity
set -e
tmp="/tmp/archivematica-sudoers"
real="/etc/sudoers.d/archivematica"
echo "archivematica ALL=NOPASSWD:/bin/mv,/bin/chown,/bin/chmod,/usr/bin/find,/usr/bin/gs,/usr/bin/inkscape" > "${tmp}"
visudo -c -f ${tmp}
if [ "$?" -eq "0" ]; then
  chown root:root "${tmp}"
  chmod 440 "${tmp}"
  mv ${tmp} ${real}
fi

# MCP Server
%post mcp-server
mkdir -p /var/log/archivematica/MCPServer
touch /var/log/archivematica/MCPServer/MCPServer.log
touch /var/log/archivematica/MCPServer/MCPServer_debug.log
chown -R archivematica:archivematica /var/log/archivematica/MCPServer

# MCP Client
%post mcp-client
mkdir -p /var/log/archivematica/MCPClient
touch /var/log/archivematica/MCPClient/MCPClient.log
touch /var/log/archivematica/MCPClient/MCPClient_debug.log
chown -R archivematica:archivematica /var/log/archivematica/MCPClient

# Dashboard
%post dashboard
export $(cat /etc/sysconfig/archivematica-dashboard)
cd /usr/share/archivematica/dashboard
/usr/share/python/archivematica-dashboard/bin/python manage.py collectstatic --noinput
mkdir -p /var/log/archivematica/dashboard
touch /var/log/archivematica/dashboard/dashboard.log
touch /var/log/archivematica/dashboard/dashboard_debug.log
chown -R archivematica:archivematica /var/log/archivematica/dashboard

# Update SELinux policy
if [ x$(semanage port -l | grep http_port_t | grep 7400 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 7400
fi
