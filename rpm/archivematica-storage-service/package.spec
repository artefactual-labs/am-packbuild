%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


Name: archivematica-storage-service
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Archivematica Storage Service
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica-storage-service/
BuildRequires: git, gcc, libffi-devel, openssl-devel, libxslt-devel, python-virtualenv, python-pip, mariadb-devel, postgresql-devel, gcc-c++
Requires: gnupg, policycoreutils-python, rng-tools, rsync, nginx, unar, p7zip, shadow-utils
AutoReq: No
AutoProv: No
%description
The Storage Service is the mechanism by which Archivematica is able to store packages and manage file locations, such as transfer source locations.


%files
/usr/share/archivematica/virtualenvs/archivematica-storage-service/
/usr/lib/archivematica/storage-service/
/var/archivematica/storage-service/
/var/archivematica/storage_service/
/usr/lib/systemd/system/archivematica-storage-service.service
%config /etc/sysconfig/archivematica-storage-service
%config /etc/nginx/conf.d/archivematica-storage-service.conf
%config /etc/archivematica/storage-service.gunicorn-config.py
%config /etc/archivematica/storageService.logging.json

%prep
rm -rf /usr/share/python/archivematica-storage-service
rm -rf /usr/share/archivematica
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone \
  --quiet \
  --branch %{_branch} \
  --depth 1 \
  --single-branch \
  --recurse-submodules \
    https://github.com/artefactual/archivematica-storage-service \
    %{_sourcedir}/%{name}


%install
mkdir -p \
  %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-storage-service/ \
  %{buildroot}/usr/lib/archivematica/storage-service/ \
  %{buildroot}/var/archivematica/storage-service/ \
  %{buildroot}/var/archivematica/storage_service/ \
  %{buildroot}/usr/lib/systemd/system \
  %{buildroot}/etc/archivematica/ \
  %{buildroot}/etc/sysconfig/ \
  %{buildroot}/etc/nginx/conf.d

virtualenv /usr/share/archivematica/virtualenvs/archivematica-storage-service
/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/pip install --upgrade pip
/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/pip install -r %{_sourcedir}/%{name}/requirements/production.txt
virtualenv --relocatable /usr/share/archivematica/virtualenvs/archivematica-storage-service
cp -rf /usr/share/archivematica/virtualenvs/archivematica-storage-service/* %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-storage-service/

cp -rf %{_sourcedir}/%{name}/storage_service/* %{buildroot}/usr/lib/archivematica/storage-service/
cp %{_sourcedir}/%{name}/install/make_key.py %{buildroot}/var/archivematica/storage-service/
cp %{_sourcedir}/%{name}/install/storage-service.gunicorn-config.py %{buildroot}/etc/archivematica/storage-service.gunicorn-config.py 
cp %{_sourcedir}/%{name}/install/storageService.logging.json %{buildroot}/etc/archivematica/storageService.logging.json
cp %{_etcdir}/archivematica-storage-service.service %{buildroot}/usr/lib/systemd/system/archivematica-storage-service.service
cp %{_etcdir}/archivematica-storage-service.env %{buildroot}/etc/sysconfig/archivematica-storage-service
cp %{_etcdir}/archivematica-storage-service.nginx %{buildroot}/etc/nginx/conf.d/archivematica-storage-service.conf


%clean
rm -rf %{buildroot}


%post

# Create archivematica user and group
getent group archivematica >/dev/null || groupadd -f -g 333 -r archivematica
if ! getent passwd archivematica >/dev/null ; then
  if ! getent passwd 333 >/dev/null ; then
    useradd -r -u 333 -g archivematica -d /var/lib/archivematica/ -s /sbin/nologin -c "Archivematica system account" -m archivematica
    else
    useradd -r -g archivematica -d /var/lib/archivematica/ -s /sbin/nologin -c "Archivematica system account" -m archivematica
    fi
fi


mkdir -p /var/log/archivematica/storage-service /var/archivematica/storage-service /var/archivematica/storage_service
touch /var/log/archivematica/storage-service/storage_service.log
touch /var/log/archivematica/storage-service/storage_service_debug.log
chown -R archivematica:archivematica /var/archivematica/storage_service /var/log/archivematica/storage-service /usr/lib/archivematica/storage-service /var/lib/archivematica /var/archivematica/storage-service
chmod 770 /var/archivematica/storage-service/
chmod 750 /var/lib/archivematica/

# Create Django secret key
KEYCMD=$(python /var/archivematica/storage-service/make_key.py 2>&1)
echo $KEYCMD
sed -i "s/<replace-with-key>/\"$KEYCMD\"/g" /etc/sysconfig/archivematica-storage-service

# Run django collectstatic task
cd /usr/lib/archivematica/storage-service
export $(cat /etc/sysconfig/archivematica-storage-service)
/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/python manage.py collectstatic --noinput --clear

systemctl daemon-reload

# Update SELinux policies
if [ x$(semanage port -l | grep http_port_t | grep 7500 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 7500
fi
if [ x$(semanage port -l | grep http_port_t | grep 8001 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 8001
fi

%changelog
* Tue Dec 11 2018 - sysadmin@artefactual.com
- Update collectstatic command: added --clear option

