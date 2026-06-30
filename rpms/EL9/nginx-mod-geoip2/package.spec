Name:           nginx-mod-geoip2

# Keep GeoIP2 module version separately
%global geoip2_version %{nginx_geoip2_version}

# Extract only the Nginx base version (e.g., "1.20.1")
%global nginx_base_version %(rpm -q --qf "%%{VERSION}" nginx-mod-devel)

# Extract the release portion (e.g., "20.el9.0.1")
%global nginx_release_version %(rpm -q --qf "%%{RELEASE}" nginx-mod-devel)

Version:        %{nginx_base_version}
Release:        %{nginx_release_version}%{?dist}
Summary:        Nginx GeoIP2 module

License:        BSD
URL:            https://github.com/leev/ngx_http_geoip2_module
Source0:        https://github.com/leev/ngx_http_geoip2_module/archive/refs/tags/%{geoip2_version}.tar.gz
BuildRequires:  nginx-mod-devel libmaxminddb-devel
Requires:       nginx >= %{nginx_base_version}, libmaxminddb

# Define the Nginx build directory
%global nginx_build_dir /usr/src/nginx-%{nginx_base_version}-%{nginx_release_version}

# Don't add /usr/lib/.build-id
#%global _build_id_links none

%description
This module adds support for the MaxMind GeoIP2 databases to Nginx.

%prep
rm -rf %{buildroot}/*
%setup -q -n ngx_http_geoip2_module-%{geoip2_version}

%build
cd %{nginx_build_dir}

./configure --with-compat --add-dynamic-module=%{_builddir}/ngx_http_geoip2_module-%{geoip2_version}

make modules

%install
mkdir -p %{buildroot}/usr/lib64/nginx/modules
cp %{nginx_build_dir}/objs/ngx_http_geoip2_module.so %{buildroot}/usr/lib64/nginx/modules/

%files
%defattr(-,root,root,-)
/usr/lib64/nginx/modules/ngx_http_geoip2_module.so

%changelog
* Mon Feb 18 2025 sysadmin@artefactual.com - %{nginx_base_version}-%{nginx_release_version}-1
- Rebuilt GeoIP2 module version %{geoip2_version} for Nginx %{nginx_base_version} on Rocky Linux 9
