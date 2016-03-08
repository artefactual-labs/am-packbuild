# Tags
Name: archivematica-storage-service-frontend
Version: 0.8.0
Release: 1
Summary: Nginx configuration file for archivematica storage service
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/archivematica-storage-service/
Requires: nginx, policycoreutils-python
AutoReq: No
AutoProv: No

%description
Django webapp for managing storage in an Archivematica

# Blocks
%files
%config /etc/nginx/conf.d/archivematica-storage-service.conf

%install

mkdir -p %{buildroot}/etc/nginx/conf.d/

cat << 'EOF' >  %{buildroot}/etc/nginx/conf.d/archivematica-storage-service.conf

server {
  listen 8001 default_server;
  client_max_body_size 4G;
  keepalive_timeout 120;
  server_name _;
  location / {
    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_redirect off;
    proxy_buffering off;
    proxy_read_timeout 120;
    proxy_pass http://localhost:7500;
  }
  location /static {
    alias /usr/share/archivematica/storage-service/static;
  }
  error_page 500 502 503 504 /500.html;
  location = /500.html {
    root /usr/share/archivematica/storage-service/templates;
  }
}
EOF


%prep
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*


%clean
rm -rf %{buildroot}

%post

echo "Update selinux policies"
if [ x$(semanage port -l | grep http_port_t | grep 8001 | wc -l) == x0 ]
	then
	semanage port -a -t http_port_t  -p tcp 8001
fi


