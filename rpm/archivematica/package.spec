%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


#
# Packages
#

Name: archivematica
Version: 1.6.0
Release: 0.beta.5
Summary: Archivematica digital preservation system
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica
BuildRequires: git, gcc, openssl-devel, python-virtualenv, python-pip, mariadb-devel, libxslt-devel, python-devel, libffi-devel, openssl-devel
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
Requires: mediainfo
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
%config /etc/archivematica/archivematicaCommon/dbsettings

# MCPServer
%files mcp-server
/usr/lib/python2.7/archivematica/MCPServer/
/usr/lib/archivematica/MCPServer/
/usr/lib/systemd/system/archivematica-mcp-server.service
/usr/share/archivematica/MCPServer/
%config /etc/sysconfig/archivematica-mcp-server
%config /etc/archivematica/MCPServer/serverConfig.conf

# MCPClient
%files mcp-client
/usr/lib/python2.7/archivematica/MCPClient/
/usr/lib/archivematica/MCPClient/
/usr/lib/systemd/system/archivematica-mcp-client.service
%config /etc/sysconfig/archivematica-mcp-client
%config /etc/archivematica/MCPClient/archivematicaClientModules
%config /etc/archivematica/MCPClient/clientConfig.conf

# Dashboard
%files dashboard
/usr/lib/python2.7/archivematica/dashboard/
/usr/share/archivematica/dashboard/
/usr/lib/systemd/system/archivematica-dashboard.service
%config /etc/sysconfig/archivematica-dashboard
%config /etc/nginx/conf.d/archivematica-dashboard.conf


#
# Preparations
#

%prep
rm -rf /usr/share/archivematica
rm -rf /usr/lib/python2.7/archivematica
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
  %{buildroot}/etc/archivematica/MCPServer \
  %{buildroot}/etc/archivematica/MCPClient \
  %{buildroot}/etc/archivematica/archivematicaCommon \
  %{buildroot}/usr/lib/archivematica/MCPServer \
  %{buildroot}/usr/lib/archivematica/MCPClient \
  %{buildroot}/usr/lib/archivematica/archivematicaCommon \
  %{buildroot}/usr/lib/python2.7/archivematica/MCPServer \
  %{buildroot}/usr/lib/python2.7/archivematica/MCPClient \
  %{buildroot}/usr/lib/python2.7/archivematica/dashboard \
  %{buildroot}/usr/share/archivematica/MCPServer \
  %{buildroot}/usr/share/archivematica/dashboard \
  %{buildroot}/var/archivematica/sharedDirectory \
  %{buildroot}/etc/sysconfig \
  %{buildroot}/usr/lib/systemd/system \
  %{buildroot}/etc/nginx/conf.d

# Common
cp -rf %{_sourcedir}/%{name}/src/archivematicaCommon/lib/* %{buildroot}/usr/lib/archivematica/archivematicaCommon/
cp -rf %{_sourcedir}/%{name}/src/archivematicaCommon/etc/* %{buildroot}/etc/archivematica/archivematicaCommon/
cp -rf %{_sourcedir}/%{name}/src/MCPServer/share/sharedDirectoryStructure/* %{buildroot}/var/archivematica/sharedDirectory/

# MCPServer
virtualenv /usr/lib/python2.7/archivematica/MCPServer
/usr/lib/python2.7/archivematica/MCPServer/bin/pip install --upgrade pip
/usr/lib/python2.7/archivematica/MCPServer/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/lib/python2.7/archivematica/MCPServer/bin/pip install -r %{_sourcedir}/%{name}/src/MCPServer/requirements/production.txt
/usr/lib/python2.7/archivematica/MCPServer/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
virtualenv --relocatable /usr/lib/python2.7/archivematica/MCPServer
cp -rf /usr/lib/python2.7/archivematica/MCPServer/* %{buildroot}/usr/lib/python2.7/archivematica/MCPServer/

cp -rf %{_sourcedir}/%{name}/src/MCPServer/lib/* %{buildroot}/usr/lib/archivematica/MCPServer/
cp -rf %{_sourcedir}/%{name}/src/MCPServer/share/* %{buildroot}/usr/share/archivematica/MCPServer/
cp %{_sourcedir}/%{name}/src/MCPServer/etc/serverConfig.conf %{buildroot}/etc/archivematica/MCPServer/serverConfig.conf
cp %{_etcdir}/archivematica-mcp-server.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-server.service
cp %{_etcdir}/archivematica-mcp-server.env %{buildroot}/etc/sysconfig/archivematica-mcp-server

# MCPClient
virtualenv /usr/lib/python2.7/archivematica/MCPClient
/usr/lib/python2.7/archivematica/MCPClient/bin/pip install --upgrade pip
/usr/lib/python2.7/archivematica/MCPClient/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/lib/python2.7/archivematica/MCPClient/bin/pip install -r %{_sourcedir}/%{name}/src/MCPClient/requirements/production.txt
/usr/lib/python2.7/archivematica/MCPClient/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
virtualenv --relocatable /usr/lib/python2.7/archivematica/MCPClient
cp -rf /usr/lib/python2.7/archivematica/MCPClient/* %{buildroot}/usr/lib/python2.7/archivematica/MCPClient/

cp -rf %{_sourcedir}/%{name}/src/MCPClient/lib/* %{buildroot}/usr/lib/archivematica/MCPClient
cp %{_sourcedir}/%{name}/src/MCPClient/etc/archivematicaClientModules %{buildroot}/etc/archivematica/MCPClient/
cp %{_sourcedir}/%{name}/src/MCPClient/etc/clientConfig.conf %{buildroot}/etc/archivematica/MCPClient/
cp %{_etcdir}/archivematica-mcp-client.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-client.service
cp %{_etcdir}/archivematica-mcp-client.env %{buildroot}/etc/sysconfig/archivematica-mcp-client

# Dashboard
virtualenv /usr/lib/python2.7/archivematica/dashboard
/usr/lib/python2.7/archivematica/dashboard/bin/pip install --upgrade pip
/usr/lib/python2.7/archivematica/dashboard/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/lib/python2.7/archivematica/dashboard/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
virtualenv --relocatable /usr/lib/python2.7/archivematica/dashboard
cp -rf /usr/lib/python2.7/archivematica/dashboard/* %{buildroot}/usr/lib/python2.7/archivematica/dashboard/

cp -rf %{_sourcedir}/%{name}/src/dashboard/src/* %{buildroot}/usr/share/archivematica/dashboard/
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
mkdir -p /var/log/archivematica/dashboard
touch /var/log/archivematica/dashboard/dashboard.log
touch /var/log/archivematica/dashboard/dashboard_debug.log
chown -R archivematica:archivematica /var/log/archivematica/dashboard

# Update SELinux policy
if [ x$(semanage port -l | grep http_port_t | grep 7400 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 7400
fi
