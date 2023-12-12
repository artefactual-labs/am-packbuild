%define _builddir ./
%define build_timestamp %(date +"%Y%m%d%H%M")

Name: enduro
Summary: A tool designed to automate the processing of transfers in multiple Archivematica pipelines
Version: %{version} 
Release: %{build_timestamp}%{?dist}
License: ASL 2.0

# BuildRequires: golang
BuildRequires: systemd-rpm-macros
BuildRequires: npm

Provides: %{name} = %{version}
%description
Enduro 

%global debug_package %{nil}

%package server
Summary: Enduro server

%description server
Enduro server

%package a3m-worker
Summary: Enduro a3m worker

%package am-worker
Summary: Enduro am worker

%description a3m-worker
Enduro A3m worker

%description am-worker
Enduro Archivematica worker

%package dashboard
Summary: Enduro dashboard

%description dashboard
Enduro dashboard website

%build
hack/build_dist.sh -o enduro ./
hack/build_dist.sh -o enduro-a3m-worker ./cmd/enduro-a3m-worker/
hack/build_dist.sh -o enduro-am-worker ./cmd/enduro-am-worker/
cd dashboard; npm install-clean; npm run build


%install 
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0755 %{name}-a3m-worker %{buildroot}%{_bindir}/%{name}-a3m-worker
install -Dpm 0755 %{name}-am-worker %{buildroot}%{_bindir}/%{name}-am-worker
install -Dpm 0755 enduro.toml %{buildroot}%{_sysconfdir}/enduro.toml
install -Dpm 0755 enduro.toml %{buildroot}%{_sysconfdir}/enduro-am-worker.toml
install -Dpm 0755 enduro.toml %{buildroot}%{_sysconfdir}/enduro-a3m-worker.toml
echo 'ENDURO_DEBUGLISTEN="127.0.0.1:9002"' > %{buildroot}%{_sysconfdir}/sysconfig/enduro-am-worker
install -Dpm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}-a3m-worker.service
install -Dpm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}-am-worker.service
mkdir -p %{buildroot}/usr/lib/enduro-dashboard
cp -a dashboard/dist/* %{buildroot}/usr/lib/enduro-dashboard/
mkdir -p %{buildroot}/var/lib/enduro
cp -a hack/sampledata/xsd/* %{buildroot}/var/lib/enduro/



%check
# go test should be here... :)

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%files server
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/enduro.toml


%files a3m-worker
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}-a3m-worker
%{_unitdir}/%{name}-a3m-worker.service
%config(noreplace) %{_sysconfdir}/enduro-a3m-worker.toml

%files am-worker
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}-am-worker
%{_unitdir}/%{name}-am-worker.service
%config(noreplace) %{_sysconfdir}/enduro-am-worker.toml
%config(noreplace) %{_sysconfdir}/sysconfig/enduro-am-worker
/var/lib/enduro/


%files dashboard
/usr/lib/enduro-dashboard/


%changelog server
* Wed May 19 2021 John Doe - 1.0-1
- First release
 
