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
/usr/share/archivematica-common
%config /etc/archivematica/archivematicaCommon/dbsettings

%install
mkdir -p %{buildroot}/usr/lib/archivematica/archivematicaCommon/
mkdir -p %{buildroot}/usr/share/archivematica-common/
mkdir -p %{buildroot}/etc/archivematica/archivematicaCommon/
cp  %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/base.txt  %{buildroot}/usr/share/archivematica-common/requirements.txt
cp -rf  %{_sourcedir}/%{name}/src/archivematicaCommon/lib/* %{buildroot}/usr/lib/archivematica/archivematicaCommon/
cp -rf  %{_sourcedir}/%{name}/src/archivematicaCommon/etc/* %{buildroot}/etc/archivematica/archivematicaCommon/


%prep
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone --branch stable/1.4.x --depth 1 --single-branch https://github.com/artefactual/archivematica %{_sourcedir}/%{name}

cd %{_sourcedir}/%{name} && git submodule init && git submodule update

%clean
rm -rf %{buildroot}

%post

