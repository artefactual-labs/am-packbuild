# Macros
%define venv_cmd virtualenv --always-copy
%define venv_name archivematica-common
%define venv_install_dir /usr/share/python/%{venv_name}
%define venv_dir %{buildroot}/%{venv_install_dir}
%define venv_bin %{venv_dir}/bin
%define venv_python %{venv_bin}/python
%define venv_pip %{venv_python} %{venv_bin}/pip install 

# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-common
Version: 1.4.1
Release: 1
BuildRoot: %(mktemp -ud %{_tmppath}/%{SOURCE0}-%{version}-%{release}-XXXXXX)
Summary: archivematica-common
Group: Application/System
License: AGPLv3

Requires: sudo, python-mimeparse, python-dateutil
AutoReq: No
AutoProv: No

# Blocks
%files
/usr/lib/archivematica/archivematicaCommon
/usr/share/archivematica-common
%config /etc/archivematica/archivematicaCommon/dbsettings

%install
#%{venv_cmd} %{venv_dir}
#%{venv_pip} -r %{_sourcedir}/%{venv_name}/src/archivematicaCommon/requirements/production.txt

mkdir -p %{buildroot}/usr/lib/archivematica/archivematicaCommon/ 
mkdir -p %{buildroot}/usr/share/archivematica-common/
mkdir -p %{buildroot}/etc/archivematica/archivematicaCommon/
cp  %{_sourcedir}/%{venv_name}/src/archivematicaCommon/requirements/base.txt  %{buildroot}/usr/share/archivematica-common/requirements.txt
cp -rf  %{_sourcedir}/%{venv_name}/src/archivematicaCommon/lib/* %{buildroot}/usr/lib/archivematica/archivematicaCommon/
cp -rf  %{_sourcedir}/%{venv_name}/src/archivematicaCommon/etc/* %{buildroot}/etc/archivematica/archivematicaCommon/


%prep
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{venv_install_dir}
mkdir -p %{buildroot}/

git clone -b stable/1.4.x --single-branch https://github.com/artefactual/archivematica %{_sourcedir}/%{venv_name}
cd %{_sourcedir}/%{venv_name} && git submodule init && git submodule update

%clean
rm -rf %{buildroot}

%post

echo "Installing python packages"
pip install -r /usr/share/archivematica-common/requirements.txt

%description
Common libraries for archivematica


