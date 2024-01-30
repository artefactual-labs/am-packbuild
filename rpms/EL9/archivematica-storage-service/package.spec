%global __brp_python_bytecompile %{nil}
%global __brp_mangle_shebangs %{nil}


Name: archivematica-storage-service
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Archivematica Storage Service
Group: Application/System
License: AGPLv3
Source0: %{git_repo}
BuildRequires: git, gcc, libffi-devel, openssl-devel, libxslt-devel, python3-virtualenv, python3-devel, mariadb-devel, postgresql-devel, gcc-c++, openldap-devel, pkgconfig
Requires: gnupg, libxslt-devel, policycoreutils-python-utils, python3-devel, rng-tools, rsync, nginx, unar, p7zip, shadow-utils, gettext
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
%config(noreplace) /etc/sysconfig/archivematica-storage-service
%config(noreplace) /etc/nginx/conf.d/archivematica-storage-service.conf
%config(noreplace) /etc/archivematica/storage-service.gunicorn-config.py
%config(noreplace) /etc/archivematica/storageService.logging.json

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
    %{git_repo} \
    %{_sourcedir}/%{name}

# This prevents build conflicts with Python packages that provide shared
# object (*.so) files and are common to AM and SS, for example lxml.
%define _build_id_links none

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
/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/pip install -r %{_sourcedir}/%{name}/requirements.txt
cp -rf /usr/share/archivematica/virtualenvs/archivematica-storage-service/* %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-storage-service/

cp -rf %{_sourcedir}/%{name}/storage_service/* %{buildroot}/usr/lib/archivematica/storage-service/
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
KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
sed -i "s/CHANGE_ME_WITH_A_SECRET_KEY/\"$KEY\"/g" /etc/sysconfig/archivematica-storage-service

systemctl daemon-reload

# Update SELinux policies
if [ x$(semanage port -l | grep http_port_t | grep 7500 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 7500
fi
if [ x$(semanage port -l | grep http_port_t | grep 8001 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 8001
fi

%posttrans
# Run django collectstatic and compilemessages.
# These tasks need to be run after postrun script on upgrades
# because the old virtualenv files need to be removed from the old package.
# https://github.com/archivematica/Issues/issues/1312
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#ordering
mkdir -p /usr/lib/archivematica/storage-service/assets
bash -c " \
  set -a -e -x
  source /etc/sysconfig/archivematica-storage-service \
    || (echo 'Environment file not found'; exit 1)
  cd /usr/lib/archivematica/storage-service
  /usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/python manage.py collectstatic --noinput --clear
  /usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/python manage.py compilemessages
";
