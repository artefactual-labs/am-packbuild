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
Source0: https://github.com/UoEMainLibrary/archivematica
BuildRequires: git, gcc, openldap-devel, openssl-devel, python-virtualenv, python-pip, mariadb-devel, libxslt-devel, python-devel, libffi-devel, openssl-devel, gcc-c++, postgresql-devel, nodejs
Requires: archivematica-common
AutoReq: No
AutoProv: No
%description
Archivematica is a web- and standards-based, open-source application which allows your institution to preserve long-term access to trustworthy, authentic and reliable digital content.

%package common
Summary: Archivematica common libraries
Requires: shadow-utils
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
Requires: tesseract
Requires: tree
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
Requires: libvpx
Requires: libraw1394
Requires: libpst
Requires: openjpeg
Requires: mediainfo
Requires: mediaconch
Requires: md5deep
Requires: uuid
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
/usr/share/archivematica/virtualenvs/archivematica-mcp-server/
/usr/lib/archivematica/MCPServer/
/usr/lib/systemd/system/archivematica-mcp-server.service
%config /etc/sysconfig/archivematica-mcp-server
%config /etc/archivematica/serverConfig.conf
%config /etc/archivematica/serverConfig.logging.json

# MCPClient
%files mcp-client
/usr/share/archivematica/virtualenvs/archivematica-mcp-client/
/usr/lib/archivematica/MCPClient/
/usr/lib/systemd/system/archivematica-mcp-client.service
%config /etc/sysconfig/archivematica-mcp-client
%config /etc/archivematica/clientConfig.conf
%config /etc/archivematica/clientConfig.logging.json

# Dashboard
%files dashboard
/usr/share/archivematica/virtualenvs/archivematica-dashboard/
/usr/share/archivematica/dashboard/
/usr/lib/systemd/system/archivematica-dashboard.service
%config /etc/sysconfig/archivematica-dashboard
%config /etc/nginx/conf.d/archivematica-dashboard.conf
%config /etc/archivematica/dashboard.gunicorn-config.py
%config /etc/archivematica/dashboard.logging.json

#
# Preparations
#

%prep
rm -rf /usr/share/python/archivematica*
rm -rf /usr/lib/archivematica
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone \
  --quiet \
  --branch %{_branch} \
  --depth 1 \
  --single-branch \
  --recurse-submodules \
    https://github.com/UoEMainLibrary/archivematica \
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
  %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-mcp-server \
  %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-mcp-client \
  %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-dashboard \
  %{buildroot}/usr/share/archivematica/dashboard \
  %{buildroot}/var/archivematica/sharedDirectory \
  %{buildroot}/etc/sysconfig \
  %{buildroot}/usr/lib/systemd/system \
  %{buildroot}/etc/nginx/conf.d

# Common
cp -rf %{_sourcedir}/%{name}/src/archivematicaCommon/lib/* %{buildroot}/usr/lib/archivematica/archivematicaCommon/

# MCPServer
virtualenv /usr/share/archivematica/virtualenvs/archivematica-mcp-server
/usr/share/archivematica/virtualenvs/archivematica-mcp-server/bin/pip install --upgrade pip
/usr/share/archivematica/virtualenvs/archivematica-mcp-server/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/share/archivematica/virtualenvs/archivematica-mcp-server/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
/usr/share/archivematica/virtualenvs/archivematica-mcp-server/bin/pip install -r %{_sourcedir}/%{name}/src/MCPServer/requirements/production.txt
virtualenv --relocatable /usr/share/archivematica/virtualenvs/archivematica-mcp-server
cp -rf /usr/share/archivematica/virtualenvs/archivematica-mcp-server/* %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-mcp-server/
cp -rf %{_sourcedir}/%{name}/src/MCPServer/lib/* %{buildroot}/usr/lib/archivematica/MCPServer/
cp %{_sourcedir}/%{name}/src/MCPServer/install/serverConfig.logging.json %{buildroot}/etc/archivematica/serverConfig.logging.json
cp %{_sourcedir}/%{name}/src/MCPServer/install/serverConfig.conf %{buildroot}/etc/archivematica/serverConfig.conf

cp %{_etcdir}/archivematica-mcp-server.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-server.service
cp %{_etcdir}/archivematica-mcp-server.env %{buildroot}/etc/sysconfig/archivematica-mcp-server

# MCPClient
virtualenv /usr/share/archivematica/virtualenvs/archivematica-mcp-client
/usr/share/archivematica/virtualenvs/archivematica-mcp-client/bin/pip install --upgrade pip
/usr/share/archivematica/virtualenvs/archivematica-mcp-client/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/share/archivematica/virtualenvs/archivematica-mcp-client/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
/usr/share/archivematica/virtualenvs/archivematica-mcp-client/bin/pip install -r %{_sourcedir}/%{name}/src/MCPClient/requirements/production.txt
virtualenv --relocatable /usr/share/archivematica/virtualenvs/archivematica-mcp-client
cp -rf /usr/share/archivematica/virtualenvs/archivematica-mcp-client/* %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-mcp-client/

cp -rf %{_sourcedir}/%{name}/src/MCPClient/lib/* %{buildroot}/usr/lib/archivematica/MCPClient
cp %{_sourcedir}/%{name}/src/MCPClient/install/clientConfig.logging.json %{buildroot}/etc/archivematica/clientConfig.logging.json
cp %{_sourcedir}/%{name}/src/MCPClient/install/clientConfig.conf %{buildroot}/etc/archivematica/clientConfig.conf
cp %{_etcdir}/archivematica-mcp-client.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-client.service
cp %{_etcdir}/archivematica-mcp-client.env %{buildroot}/etc/sysconfig/archivematica-mcp-client

# Dashboard
virtualenv /usr/share/archivematica/virtualenvs/archivematica-dashboard
/usr/share/archivematica/virtualenvs/archivematica-dashboard/bin/pip install --upgrade pip
/usr/share/archivematica/virtualenvs/archivematica-dashboard/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/share/archivematica/virtualenvs/archivematica-dashboard/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
virtualenv --relocatable /usr/share/archivematica/virtualenvs/archivematica-dashboard
cd %{_sourcedir}/%{name}/src/dashboard/frontend/transfer-browser/ && npm install --unsafe-perm 

cd %{_sourcedir}/%{name}/src/dashboard/frontend/appraisal-tab/ && npm install --unsafe-perm

find %{_sourcedir}/%{name}/src/dashboard/ | grep static
cp -rf /usr/share/archivematica/virtualenvs/archivematica-dashboard/* %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-dashboard/

cp -rf %{_sourcedir}/%{name}/src/dashboard/src/* %{buildroot}/usr/share/archivematica/dashboard/
cp %{_sourcedir}/%{name}/src/dashboard/install/dashboard.gunicorn-config.py %{buildroot}/etc/archivematica/dashboard.gunicorn-config.py
cp %{_sourcedir}/%{name}/src/dashboard/install/dashboard.logging.json %{buildroot}/etc/archivematica/dashboard.logging.json
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

# MCP Server
%post mcp-server
mkdir -p /var/log/archivematica/MCPServer
chown -R archivematica:archivematica /var/log/archivematica/MCPServer
systemctl daemon-reload

# MCP Client
%post mcp-client
mkdir -p /var/log/archivematica/MCPClient
chown -R archivematica:archivematica /var/log/archivematica/MCPClient
systemctl daemon-reload

# Dashboard
%post dashboard

mkdir -p /var/log/archivematica/dashboard

# Create Django key
KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
sed -i "s/CHANGE_ME_WITH_A_SECRET_KEY/\"$KEY\"/g" /etc/sysconfig/archivematica-dashboard

# Run django collectstatic
mkdir -p /usr/share/archivematica/dashboard/static
export $(cat /etc/sysconfig/archivematica-dashboard)
cd /usr/share/archivematica/dashboard
/usr/share/archivematica/virtualenvs/archivematica-dashboard/bin/python manage.py collectstatic --noinput --clear

chown -R archivematica:archivematica /var/log/archivematica/dashboard
systemctl daemon-reload
# Update SELinux policy
if [ x$(semanage port -l | grep http_port_t | grep 7400 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 7400
fi

%changelog
* Wed Jan 09 2019 - sysadmin@artefactual.com
- Create collectstatic directory in post script
* Tue Dec 11 2018 - sysadmin@artefactual.com
- Update collectstatic command: added --clear option

