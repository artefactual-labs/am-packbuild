# Macros
%define venv_cmd virtualenv --always-copy
%define venv_name archivematica-mcp-client
%define venv_install_dir /usr/share/python/%{venv_name}
%define venv_dir %{buildroot}/%{venv_install_dir}
%define venv_bin %{venv_dir}/bin
%define venv_python %{venv_bin}/python
%define venv_pip %{venv_python} %{venv_bin}/pip install 

# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-mcp-client
Version: 1.4.1
Release: 1
BuildRoot: %(mktemp -ud %{_tmppath}/%{SOURCE0}-%{version}-%{release}-XXXXXX)
Summary: archivematica-mcp-client
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica/
Requires: sudo, tesseract, p7zip, ImageMagick, ghostscript, perl-Image-ExifTool, inkscape
AutoReq: No
AutoProv: No

# Blocks
%files
/usr/lib/archivematica/MCPClient/
/usr/lib/systemd/system/archivematica-mcp-client.service
%config /etc/archivematica/MCPClient/archivematicaClientModules
%config /etc/archivematica/MCPClient/clientConfig.conf
%config /etc/init/archivematica-mcp-client.conf
%config /etc/init.d/archivematica-mcp-clientd

%install

mkdir -p %{buildroot}/etc/archivematica/MCPClient %{buildroot}/etc/init/ %{buildroot}/etc/init.d/ %{buildroot}//usr/lib/archivematica/MCPClient

cp  %{_sourcedir}/%{venv_name}/src/MCPClient/etc/archivematicaClientModules %{buildroot}/etc/archivematica/MCPClient/
cp  %{_sourcedir}/%{venv_name}/src/MCPClient/etc/clientConfig.conf %{buildroot}/etc/archivematica/MCPClient/
cp -rf  %{_sourcedir}/%{venv_name}/src/MCPClient/init/* %{buildroot}/etc/init/
cp -rf  %{_sourcedir}/%{venv_name}/src/MCPClient/init.d/* %{buildroot}/etc/init.d/
cp -rf  %{_sourcedir}/%{venv_name}/src/MCPClient/lib/* %{buildroot}/usr/lib/archivematica/MCPClient

mkdir -p %{buildroot}/usr/lib/systemd/system/
cat << EOF > %{buildroot}/usr/lib/systemd/system/archivematica-mcp-client.service
[Unit]
Description=Archivematica MCP Client
After=syslog.target network.target

[Service]
User=archivematica
ExecStart=/usr/bin/python /usr/lib/archivematica/MCPClient/archivematicaClient.py

[Install]
WantedBy=multi-user.target

EOF

%prep
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{venv_install_dir}

git clone -b stable/1.4.x --single-branch https://github.com/artefactual/archivematica %{_sourcedir}/%{venv_name}
cd %{_sourcedir}/%{venv_name} && git submodule init && git submodule update

%clean
rm -rf %{buildroot}

%post
echo "creating archivematica user"
userID=`id -u archivematica`

if [ "${userID}" = 333 ]; then
  echo "User archivematica exists"
else
  useradd --uid 333 -U --home /var/lib/archivematica/ archivematica
fi

logdir=/var/log/archivematica/MCPClient
sudo mkdir -p $logdir
sudo chown -R archivematica:archivematica $logdir
sudo chmod -R g+ws $logdir


%description
MCP Client for Archivematica

