# Macros
%define venv_cmd virtualenv --always-copy
%define venv_name archivematica-storage-service
%define venv_install_dir /usr/share/python/%{venv_name}
%define venv_dir %{buildroot}/%{venv_install_dir}
%define venv_bin %{venv_dir}/bin
%define venv_python %{venv_bin}/python
%define venv_pip %{venv_python} %{venv_bin}/pip install 

# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-storage-service
Version: 0.6.1
Release: 1
BuildRoot: %(mktemp -ud %{_tmppath}/%{SOURCE0}-%{version}-%{release}-XXXXXX)
Summary: archivematica-storage-service
Group: Application/System
License: AGPLv3
#Source0: https://github.com/artefactual/archivematica-storage-service/archive/qa/0.x.tar.gz
#Source0: 0.x.tar.gz
Requires: rsync, python-lxml, nginx, uwsgi, uwsgi-plugin-python
AutoReq: No
AutoProv: No

# Blocks
%files
/%{venv_install_dir}
/etc/uwsgi/apps-available/*
/etc/nginx/sites-available/*
/var/archivematica/*
/usr/share/archivematica/
/var/archivematica/storage-service/*
/var/archivematica/.storage-service

%install
%{venv_cmd} %{venv_dir}
%{venv_pip} -r %{_sourcedir}/%{venv_name}/requirements/production.txt
cd %{_sourcedir}/%{venv_name}
%{venv_python} setup.py install
mkdir -p  %{buildroot}/etc/uwsgi/apps-available/
mkdir -p  %{buildroot}/etc/nginx/sites-available/
mkdir -p  %{buildroot}var/archivematica/
mkdir -p  %{buildroot}/var/archivematica/storage-service/
mkdir -p  %{buildroot}/usr/share/archivematica
cp install/storage.ini  %{buildroot}/etc/uwsgi/apps-available/
cp install/storage  %{buildroot}/etc/nginx/sites-available/
cp install/.storage-service  %{buildroot}/var/archivematica/
cp install/make_key.py  %{buildroot}/var/archivematica/storage-service/
cp -rf storage_service/static storage_service/templates %{buildroot}/usr/share/python/archivematica-storage-service/lib/python2.7/site-packages/archivematica_storage_service-0.6.1-py2.7.egg/storage_service

## Problems with symbolic links, we remove the link and put the file in place
rm %{buildroot}/usr/share/python/archivematica-storage-service/lib/python2.7/site-packages/archivematica_storage_service-0.6.1-py2.7.egg/storage_service/static/js/vendor/base64.js
cp storage_service/external/base64-helpers/base64-helpers.js %{buildroot}/usr/share/python/archivematica-storage-service/lib/python2.7/site-packages/archivematica_storage_service-0.6.1-py2.7.egg/storage_service/static/js/vendor/base64.js

cd -
# RECORD files are used by wheels for checksum. They contain path names which
# match the buildroot and must be removed or the package will fail to build.
find %{buildroot} -name "RECORD" -exec rm -rf {} \;
# Change the virtualenv path to the target installation direcotry.
venvctrl-relocate --source=%{venv_dir} --destination=/%{venv_install_dir}

%prep
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{venv_install_dir}
mkdir -p %{buildroot}/
#git clone -b qa/0.x --single-branch https://github.com/artefactual/archivematica-storage-service %{buildroot}/%{venv_install_dir}/
git clone -b qa/0.x --single-branch https://github.com/artefactual/archivematica-storage-service %{_sourcedir}/%{venv_name}
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


echo "creating django secret key"
KEYCMD=$(python /var/archivematica/storage-service/make_key.py 2>&1)
echo $KEYCMD

sed -i "s/<replace-with-key>/\"$KEYCMD\"/g" /var/archivematica/.storage-service
sed -i "s/<replace-with-key>/\"$KEYCMD\"/g" /etc/uwsgi/apps-available/storage.ini

. /var/archivematica/.storage-service

echo "creating symlink in /usr/lib/archivematica"
rm -f /usr/lib/archivematica/storage-service
#ln -s -f /usr/share/python/archivematica-storage-service/storage_service/ /usr/lib/archivematica/storage-service
mkdir -p /usr/lib/archivematica
ln -s -f /usr/share/python/archivematica-storage-service/lib/python2.7/site-packages/archivematica_storage_service-0.6.1-py2.7.egg/storage_service /usr/lib/archivematica/storage-service

rsync -a /usr/lib/archivematica/storage-service/static /usr/lib/archivematica/storage-service
rsync -a //usr/lib/archivematica/storage-service/templates /usr/lib/archivematica/storage-service

cd /usr/lib/archivematica/storage-service

#echo "installing swift dependencies"
#/usr/share/python/archivematica-storage-service/bin/pip install python-swiftclient
#/usr/share/python/archivematica-storage-service/bin/pip install python-keystoneclienta
export PYTHONPATH=/usr/share/python/archivematica-storage-service/lib/python2.7/site-packages/
echo "creating log directories"
mkdir -p /var/log/archivematica/storage-service
touch /var/log/archivematica/storage-service/storage_service.log
echo "configuring django database and static files"
/usr/share/python/archivematica-storage-service/bin/python manage.py syncdb
/usr/share/python/archivematica-storage-service/bin/python manage.py migrate
/usr/share/python/archivematica-storage-service/bin/python manage.py collectstatic --noinput

echo "create /var/archivematica/storage_service directory"
mkdir -p /var/archivematica/storage_service

echo "updating directory permissions"
chown -R archivematica:archivematica /var/archivematica/storage-service
chown -R archivematica:archivematica /var/archivematica/storage_service
chown -R archivematica:archivematica /var/archivematica/.storage-service
chown -R archivematica:archivematica /usr/share/python/archivematica-storage-service
chown -R archivematica:archivematica /var/log/archivematica/storage-service

rm -f /tmp/storage_service.log


%description
Django webapp for managing storage in an Archivematica

