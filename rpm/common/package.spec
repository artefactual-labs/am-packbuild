# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-common
Version: 1.4.1
Release: 1
Summary: Archivematica common files
Group: Application/System
License: AGPLv3
BuildRequires: git
Source0: https://github.com/artefactual/archivematica/
AutoReq: No
AutoProv: No

%description
Common files for Archivematica

# Blocks
%files
/usr/lib/archivematica/archivematicaCommon/
/var/archivematica/sharedDirectory
/usr/share/archivematica-common
%config /etc/archivematica/archivematicaCommon/dbsettings

%install

mkdir -p %{buildroot}/usr/share/archivematica-common/
cp  %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/base.txt  %{buildroot}/usr/share/archivematica-common/requirements.txt

mkdir -p %{buildroot}/usr/lib/archivematica/archivematicaCommon/
cp -rf  %{_sourcedir}/%{name}/src/archivematicaCommon/lib/* %{buildroot}/usr/lib/archivematica/archivematicaCommon/

mkdir -p %{buildroot}/etc/archivematica/archivematicaCommon/
cp -rf  %{_sourcedir}/%{name}/src/archivematicaCommon/etc/* %{buildroot}/etc/archivematica/archivematicaCommon/

mkdir -p %{buildroot}/var/archivematica/sharedDirectory
cp -rf %{_sourcedir}/%{name}/src/MCPServer/share/sharedDirectoryStructure/* %{buildroot}/var/archivematica/sharedDirectory/

%prep
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

chown -R archivematica:archivematica /var/archivematica/sharedDirectory
