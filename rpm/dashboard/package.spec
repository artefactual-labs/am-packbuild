# Globals
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# Tags
Name: archivematica-dashboard
Version: 1.4.1
Release: 1
Summary: Archivematica dashboard
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica/
BuildRequires: git, gcc, openssl-devel, python-virtualenv, python-pip, mariadb-devel
AutoReq: No
AutoProv: No

%description


# Blocks
%files
/usr/share/archivematica/dashboard
/usr/lib/systemd/system/archivematica-dashboard.service
/usr/lib/python2.7/archivematica/dashboard


%install

mkdir -p %{buildroot}/usr/lib/python2.7/archivematica/dashboard
virtualenv /usr/lib/python2.7/archivematica/dashboard
/usr/lib/python2.7/archivematica/dashboard/bin/pip install --upgrade pip
/usr/lib/python2.7/archivematica/dashboard/bin/pip install -r %{_sourcedir}/%{name}/src/archivematicaCommon/requirements/production.txt
/usr/lib/python2.7/archivematica/dashboard/bin/pip install -r %{_sourcedir}/%{name}/src/dashboard/src/requirements/production.txt
/usr/lib/python2.7/archivematica/dashboard/bin/pip install mysql
virtualenv --relocatable /usr/lib/python2.7/archivematica/dashboard
cp -rf /usr/lib/python2.7/archivematica/dashboard/* %{buildroot}/usr/lib/python2.7/archivematica/dashboard/

mkdir -p %{buildroot}/usr/share/archivematica/dashboard
cp -rf %{_sourcedir}/%{name}/src/dashboard/src/* %{buildroot}/usr/share/archivematica/dashboard/

mkdir -p %{buildroot}/usr/lib/systemd/system/
cat << EOF > %{buildroot}/usr/lib/systemd/system/archivematica-dashboard.service
[Unit]
Description=Archivematica MCP Server
After=syslog.target network.target

[Service]
PIDFile=/run/archivematica-dashboard_gunicorn.pid
User=archivematicadashboard
Group=archivematicadashboard
EnvironmentFile=-/etc/sysconfig/archivematica-dashboard
WorkingDirectory=/usr/share/archivematica/dashboard/
ExecStart=/usr/lib/python2.7/archivematica/dashboard/bin/gunicorn --workers 2 --timeout 120 --access-logfile /var/log/archivematica/dashboard/gunicorn.log --error-logfile /var/log/archivematica/dashboard/gunicorn_error.log --log-level error --bind localhost:7600 wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

cat << EOF > %{buildroot}/etc/sysconfig/archivematica-dashboard

EOF
%prep
rm -rf /usr/share/archivematica
rm -rf /usr/lib/python2.7/archivematica
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone --branch stable/1.4.x --depth 1 --single-branch https://github.com/artefactual/archivematica %{_sourcedir}/%{name}

cd %{_sourcedir}/%{name} && git submodule init && git submodule update

%clean
rm -rf %{buildroot}

%post
echo "Creating archivematicadashboard user"
userID=`id -u archivematicadashboard`

if [ "${userID}" = 334 ]; then
  echo "User archivematicadashboard exists"
else
  useradd --uid 334 --user-group --home /var/lib/archivematica/ archivematica
fi

echo "Update SELinux policies"
if [ x$(semanage port -l | grep http_port_t | grep 7600 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 7600
fi


