# Macros
%define venv_cmd virtualenv --always-copy
%define venv_name dashboard
%define venv_install_dir /usr/share/archivematica/%{venv_name}
%define venv_dir %{buildroot}/%{venv_install_dir}
%define venv_bin %{venv_dir}/bin
%define venv_python %{venv_bin}/python
%define venv_pip %{venv_python} %{venv_bin}/pip install 

# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-dashboard
Version: 1.4.1
Release: 1
BuildRoot: %(mktemp -ud %{_tmppath}/%{SOURCE0}-%{version}-%{release}-XXXXXX)
Summary: archivematica-dashboard
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica/
Requires: archivematica-common, MySQL-python, httpd, mod_wsgi
AutoReq: No
AutoProv: No

# Blocks
%files
/usr/share/archivematica/dashboard
/usr/lib/archivematica-dashboard
%config /etc/httpd/conf.d/archivematica-dashboard.conf
%install
mkdir -p %{buildroot}/usr/share/archivematica/dashboard/
mkdir -p %{buildroot}/usr/lib/archivematica-dashboard

#pip install -t %{buildroot}/usr/lib/archivematica-dashboard -r %{_sourcedir}/%{venv_name}/src/dashboard/src/requirements/production.txt

mkdir -p %{buildroot}/usr/share/archivematica/dashboard
cp -rf %{_sourcedir}/%{venv_name}/src/dashboard/src/* %{buildroot}/usr/share/archivematica/dashboard/

mkdir -p %{buildroot}/etc/httpd/conf.d/
cp  %{_sourcedir}/%{venv_name}/localDevSetup/apache/apache.default %{buildroot}/etc/httpd/conf.d/archivematica-dashboard.conf

#Update apache config for apache > 2.4
sed -i 's/Order allow,deny//g' %{buildroot}/etc/httpd/conf.d/archivematica-dashboard.conf
sed -i 's/Allow from all/Require all granted/g' %{buildroot}/etc/httpd/conf.d/archivematica-dashboard.conf


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
echo "creating archivematicadashboard user"
userID=`id -u archivematicadashboard`

if [ "${userID}" = 334 ]; then
  echo "User archivematicadashboard exists"
else
  useradd --uid 334 -U --home /var/lib/archivematica-django/ archivematicadashboard
fi

logdir=/var/log/archivematica/dashboard
mkdir -p $logdir
touch $logdir/dashboard.log
chown -R archivematicadashboard:archivematica $logdir
chmod -R g+ws $logdir

#install dashboard requirements
pip install -r /usr/share/archivematica/dashboard/requirements.txt

#Install gearman too (add to requirements?)
pip install gearman
echo "Don't forget to run migrations with:"
echo sudo -u archivematicadashboard /usr/share/archivematica/dashboard/manage.py syncdb --settings='settings.common'

%description
Archivematica dashboard


