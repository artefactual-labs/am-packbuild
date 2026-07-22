%global __brp_python_bytecompile %{nil}
%global __brp_mangle_shebangs %{nil}


Name: archivematica-storage-service
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Archivematica Storage Service
Group: Application/System
License: AGPLv3
Source0: %{git_repo}
BuildRequires: git, gcc, libffi-devel, openssl-devel, libxslt-devel, python3-virtualenv, python3.12-devel, mariadb-devel, postgresql-devel, gcc-c++, openldap-devel, nodejs >= 24, pkgconfig
Requires: gnupg, libxslt-devel, mariadb-connector-c, policycoreutils-python-utils, python3.12-devel, rng-tools, rsync, nginx, unar, p7zip, shadow-utils, gettext
AutoReq: No
AutoProv: No
%description
The Storage Service is the mechanism by which Archivematica is able to store packages and manage file locations, such as transfer source locations.

%files
/usr/share/archivematica/virtualenvs/archivematica-storage-service/
/opt/archivematica/archivematica-storage-service/
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
  %{buildroot}/opt/archivematica/archivematica-storage-service/src/archivematica/storage_service/assets \
  %{buildroot}/opt/archivematica/archivematica-storage-service/src/archivematica/storage_service/frontend/dist/ \
  %{buildroot}/var/archivematica/storage-service/ \
  %{buildroot}/var/archivematica/storage_service/ \
  %{buildroot}/usr/lib/systemd/system \
  %{buildroot}/etc/archivematica/ \
  %{buildroot}/etc/sysconfig/ \
  %{buildroot}/etc/nginx/conf.d

# Create runtime source directory under /opt and make the same path available in
# the buildroot. This path is used for editable install.
mkdir -p /opt/archivematica/archivematica-storage-service
cp -rf %{_sourcedir}/%{name}/. /opt/archivematica/archivematica-storage-service/
cp -rf %{_sourcedir}/%{name}/. %{buildroot}/opt/archivematica/archivematica-storage-service/

virtualenv --python=python3.12 /usr/share/archivematica/virtualenvs/archivematica-storage-service
/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/pip install --upgrade pip setuptools
UV_PYTHON=python3.12 UV_PYTHON_DOWNLOADS=never \
  uv export --project %{_sourcedir}/%{name} --locked --no-dev --no-hashes \
    --no-emit-project --output-file %{_builddir}/uv-runtime-requirements.txt
/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/pip install -r %{_builddir}/uv-runtime-requirements.txt

# Install the application in editable mode so the source directory under /opt is
# importable by the virtualenv at runtime.
/usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/pip install --no-deps --editable /opt/archivematica/archivematica-storage-service
cp -rf /usr/share/archivematica/virtualenvs/archivematica-storage-service/* %{buildroot}/usr/share/archivematica/virtualenvs/archivematica-storage-service/

cp %{_sourcedir}/%{name}/install/storage-service.gunicorn-config.py %{buildroot}/etc/archivematica/storage-service.gunicorn-config.py
cp %{_sourcedir}/%{name}/install/storageService.logging.json %{buildroot}/etc/archivematica/storageService.logging.json
cp %{_etcdir}/archivematica-storage-service.service %{buildroot}/usr/lib/systemd/system/archivematica-storage-service.service
cp %{_etcdir}/archivematica-storage-service.env %{buildroot}/etc/sysconfig/archivematica-storage-service
cp %{_etcdir}/archivematica-storage-service.nginx %{buildroot}/etc/nginx/conf.d/archivematica-storage-service.conf

cd %{_sourcedir}/%{name}/src/archivematica/storage_service/frontend/ && npm clean-install --unsafe-perm
cd %{_sourcedir}/%{name}/src/archivematica/storage_service/frontend/ && npm run build
test -d %{_sourcedir}/%{name}/src/archivematica/storage_service/frontend/dist
cp -a %{_sourcedir}/%{name}/src/archivematica/storage_service/frontend/dist/. %{buildroot}/opt/archivematica/archivematica-storage-service/src/archivematica/storage_service/frontend/dist/


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
chown -R archivematica:archivematica /var/archivematica/storage_service /var/log/archivematica/storage-service /var/lib/archivematica /var/archivematica/storage-service
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
if [ -f /etc/sysconfig/archivematica-storage-service ]; then
  if grep -Eq '^DJANGO_SETTINGS_MODULE="?storage_service.settings.production"?$' /etc/sysconfig/archivematica-storage-service; then
    sed -i 's#^DJANGO_SETTINGS_MODULE=.*#DJANGO_SETTINGS_MODULE=archivematica.storage_service.storage_service.settings.production#' /etc/sysconfig/archivematica-storage-service
  fi
  if grep -Eq '^PYTHONPATH="?/usr/lib/archivematica/storage-service"?$' /etc/sysconfig/archivematica-storage-service; then
    sed -i -E '/^PYTHONPATH="?\/usr\/lib\/archivematica\/storage-service"?$/d' /etc/sysconfig/archivematica-storage-service
  fi
  if grep -Eq '^DJANGO_STATIC_ROOT="?/usr/lib/archivematica/storage-service/assets"?$' /etc/sysconfig/archivematica-storage-service; then
    sed -i 's#^DJANGO_STATIC_ROOT=.*#DJANGO_STATIC_ROOT=/opt/archivematica/archivematica-storage-service/src/archivematica/storage_service/assets#' /etc/sysconfig/archivematica-storage-service
  fi
fi
# Run django collectstatic and compilemessages.
# These tasks need to be run after postrun script on upgrades
# because the old virtualenv files need to be removed from the old package.
# https://github.com/archivematica/Issues/issues/1312
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#ordering
mkdir -p /opt/archivematica/archivematica-storage-service/src/archivematica/storage_service/assets
bash -c " \
  set -a -e -x
  source /etc/sysconfig/archivematica-storage-service \
    || (echo 'Environment file not found'; exit 1)
  cd /opt/archivematica/archivematica-storage-service/
  /usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/python -m archivematica.storage_service.manage collectstatic --noinput --clear
  /usr/share/archivematica/virtualenvs/archivematica-storage-service/bin/python -m archivematica.storage_service.manage compilemessages
";
chown -R archivematica:archivematica /opt/archivematica/archivematica-storage-service/src/archivematica/storage_service/assets
chown -R archivematica:archivematica /opt/archivematica/archivematica-storage-service/src/archivematica/storage_service/locale
