# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-mcp-server
Version: 1.4.1
Release: 1
Summary: Archivematica MCP Server
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica/
BuildRequires: git, gcc, openssl-devel, python-virtualenv, python-pip
Requires: mariadb-server,gearmand
AutoReq: No
AutoProv: No

%description


# Blocks
%files
/usr/share/archivematica/
/usr/lib/archivematica/MCPServer
/usr/lib/python2.7/archivematica/MCPServer
/usr/lib/systemd/system/archivematica-mcp-server.service
%config /etc/serverConfig.conf

%install

mkdir -p %{buildroot}/usr/lib/python2.7/archivematica/MCPServer
virtualenv /usr/lib/python2.7/archivematica/MCPServer
/usr/lib/python2.7/archivematica/MCPServer/bin/pip install --upgrade pip
/usr/lib/python2.7/archivematica/MCPServer/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
virtualenv --relocatable /usr/lib/python2.7/archivematica/MCPServer/
cp -rf /usr/lib/python2.7/archivematica/MCPServer/* %{buildroot}/usr/lib/python2.7/archivematica/MCPServer/

mkdir -p %{buildroot}/usr/lib/archivematica/MCPServer
cp %{_sourcedir}/%{name}/src/MCPServer/lib/* %{buildroot}/usr/lib/archivematica/MCPServer/

mkdir -p %{buildroot}/usr/share/archivematica
cp -rf  %{_sourcedir}/%{name}/src/MCPServer/share/* %{buildroot}/usr/share/archivematica/

mkdir -p %{buildroot}/etc
cp  %{_sourcedir}/%{name}/src/MCPServer/etc/serverConfig.conf %{buildroot}/etc/serverConfig.conf

mkdir -p %{buildroot}/usr/lib/systemd/system/
cat << EOF > %{buildroot}/usr/lib/systemd/system/archivematica-mcp-server.service
[Unit]
Description=Archivematica MCP Server
After=syslog.target network.target

[Service]
User=archivematica
ExecStart=/usr/lib/python2.7/archivematica/MCPServer/bin/python /usr/lib/archivematica/MCPServer/archivematicaMCP.py

[Install]
WantedBy=multi-user.target
EOF


%prep
rm -rf /usr/share/archivematica
rm -rf /usr/lib/python2.7/archivematica
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone --branch stable/1.4.x --depth 1 --single-branch https://github.com/artefactual/archivematica %{_sourcedir}/%{name}

cd %{_sourcedir}/%{name} && git submodule init && git submodule update

%clean
rm -rf %{buildroot}

%post
echo "Creating archivematica user"
userID=`id -u archivematica`

if [ "${userID}" = 333 ]; then
  echo "User archivematica exists"
else
  useradd --uid 333 --user-group --home /var/lib/archivematica/ archivematica
fi


