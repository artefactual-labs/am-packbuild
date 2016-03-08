# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-storage-service
Version: 0.6.1
Release: 1
Summary: Archivematica storage service
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica-storage-service/
BuildRequires: git, gcc, libffi-devel, openssl-devel, libxslt-devel,python-virtualenv, python-pip
Requires: unar
AutoReq: No
AutoProv: No

%description
Django webapp for managing storage in an Archivematica

# Blocks
%files
/usr/share/archivematica/storage-service/
/usr/lib/archivematica/storage-service/
/var/archivematica/*
/var/archivematica/storage-service/*
/usr/lib/systemd/system/archivematica-storage-service.service
%config /etc/sysconfig/archivematica-storage-service

%install

mkdir -p %{buildroot}/usr/share/archivematica/storage-service/
mkdir -p %{buildroot}/usr/lib/archivematica/storage-service/

#We build the virtualenv in place, and then move it
# This avoids problems with the buildpath found inside .so files
virtualenv /usr/lib/archivematica/storage-service

/usr/lib/archivematica/storage-service/bin/pip install --upgrade pip

/usr/lib/archivematica/storage-service/bin/pip install -r %{_sourcedir}/%{name}/requirements/production.txt

virtualenv --relocatable /usr/lib/archivematica/storage-service/
cp -rf /usr/lib/archivematica/storage-service/* %{buildroot}/usr/lib/archivematica/storage-service/
cp -rf %{_sourcedir}/%{name}/storage_service/*  %{buildroot}/usr/share/archivematica/storage-service



mkdir -p  %{buildroot}/var/archivematica/storage-service/
cp %{_sourcedir}/%{name}/install/make_key.py  %{buildroot}/var/archivematica/storage-service/

mkdir -p  %{buildroot}/etc/sysconfig/
cp %{_sourcedir}/%{name}/install/.storage-service  %{buildroot}/etc/sysconfig/archivematica-storage-service
sed -i '/^alias/d' %{buildroot}/etc/sysconfig/archivematica-storage-service
sed -i 's/export //g' %{buildroot}/etc/sysconfig/archivematica-storage-service

#Create systemd script
mkdir -p %{buildroot}/usr/lib/systemd/system/
cat << EOF > %{buildroot}/usr/lib/systemd/system/archivematica-storage-service.service
[Unit]
Description=archivematica storage daemon
After=network.target

[Service]

PIDFile=/run/gunicorn/pid
User=archivematica
Group=archivematica
EnvironmentFile=-/etc/sysconfig/archivematica-storage-service
WorkingDirectory=/usr/share/archivematica/storage-service/
ExecStart=/usr/lib/archivematica/storage-service/bin/gunicorn  --workers 2 --timeout 120 --access-logfile /var/log/archivematica/storage-service/gunicorn.log --error-logfile /var/log/archivematica/storage-service/gunicorn_error.log --log-level error --bind localhost:7500 storage_service.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

%prep
rm -rf /usr/share/archivematica
rm -rf /usr/lib/archivematica
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone -b qa/0.x --single-branch https://github.com/artefactual/archivematica-storage-service %{_sourcedir}/%{name}

cd %{_sourcedir}/%{name} && git submodule init && git submodule update

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

sed -i "s/<replace-with-key>/\"$KEYCMD\"/g" /etc/sysconfig/archivematica-storage-service


echo "creating log directories"
mkdir -p /var/log/archivematica/storage-service
touch /var/log/archivematica/storage-service/storage_service.log
touch /var/log/archivematica/storage-service/storage_service_debug.log

#echo "configuring django database and static files"
#/usr/share/python/archivematica-storage-service/bin/python manage.py syncdb
#/usr/share/python/archivematica-storage-service/bin/python manage.py migrate
#/usr/share/python/archivematica-storage-service/bin/python manage.py collectstatic --noinput

echo "create /var/archivematica/storage_service directory"
mkdir -p /var/archivematica/storage_service

echo "updating directory permissions"
chown -R archivematica:archivematica /var/archivematica/storage-service
chown -R archivematica:archivematica /var/log/archivematica/storage-service
chown -R archivematica:archivematica /usr/share/archivematica/storage-service
chmod 750 /var/lib/archivematica/
chown -R archivematica:archivematica /var/lib/archivematica/

rm -f /tmp/storage_service.log



