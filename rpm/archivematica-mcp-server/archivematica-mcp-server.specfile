# Macros
%define venv_cmd virtualenv --always-copy
%define venv_name archivematica-mcp-server
%define venv_install_dir /usr/share/python/%{venv_name}
%define venv_dir %{buildroot}/%{venv_install_dir}
%define venv_bin %{venv_dir}/bin
%define venv_python %{venv_bin}/python
%define venv_pip %{venv_python} %{venv_bin}/pip install 

# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-mcp-server
Version: 1.4.1
Release: 1
BuildRoot: %(mktemp -ud %{_tmppath}/%{SOURCE0}-%{version}-%{release}-XXXXXX)
Summary: archivematica-mcp-server
Group: Application/System
License: AGPLv3
#Source0: https://github.com/artefactual/archivematica-mcp-server/archive/qa/0.x.tar.gz
#Source0: 0.x.tar.gz
Requires: sudo, gearmand, uuid
AutoReq: No
AutoProv: No

# Blocks
%files
/usr/share/archivematica/
/usr/lib/archivematica/MCPServer
%config /etc/serverConfig.conf
/init.d/archivematica-mcp-serverd
/init/archivematica-mcp-server.conf

%install
mkdir -p %{buildroot}/etc/ %{buildroot}/init/  %{buildroot}/init.d/ %{buildroot}//usr/lib/archivematica/MCPServer

cp -rf  %{_sourcedir}/%{venv_name}/src/MCPServer/etc/* %{buildroot}/etc/
cp -rf  %{_sourcedir}/%{venv_name}/src/MCPServer/init/* %{buildroot}/init/
cp -rf  %{_sourcedir}/%{venv_name}/src/MCPServer/init.d/* %{buildroot}/init.d/
mkdir -p %{buildroot}/usr/share/archivematica/
cp -rf  %{_sourcedir}/%{venv_name}/src/MCPServer/share/* %{buildroot}/usr/share/archivematica/
cp -rf  %{_sourcedir}/%{venv_name}/src/MCPServer/lib/* %{buildroot}/usr/lib/archivematica/MCPServer


%prep
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{venv_install_dir}
mkdir -p %{buildroot}/
#git clone --depth=1 --recurse-submodules --branch ${BRANCH} https://github.com/artefactual/archivematica.git %{_sourcedir}/%{venv_name}
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

if [ -d /var/archivematica/sharedDirectory ]; then
  echo "/var/archivematica/sharedDirectory exists"
else
  echo "/var/archivematica/sharedDirectory doesn't exist... creating..."
  mkdir -p /var/archivematica/sharedDirectory/
  rsync -a /usr/share/archivematica/sharedDirectoryStructure/* /var/archivematica/sharedDirectory/.
fi

chown -R archivematica:archivematica /var/archivematica/sharedDirectory/

logdir=/var/log/archivematica/MCPServer
sudo mkdir -p $logdir
sudo chown -R archivematica:archivematica $logdir
sudo chmod -R g+ws $logdir

/usr/share/archivematica/postinstSharedWithDev


%description
MCP Server for Archivematica


