%define _builddir ./
%define build_timestamp %(date +"%Y%m%d%H%M")

Name: preprocessing-worker
Summary: A tool designed to run custom SFA workflows
Version: %{version} 
Release: %{build_timestamp}%{?dist}
License: ASL 2.0

# BuildRequires: golang
BuildRequires: systemd-rpm-macros

Provides: %{name} = %{version}
%description
Enduro 

%global debug_package %{nil}


%package preprocessing-worker
Summary: preprocessing am worker

%description preprocessing-worker
Preprocessing worker

%build
hack/build_dist.sh -o preprocessing-worker ./cmd/worker/


%install 
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service



%check
# go test should be here... :)

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service


%files preprocessing-worker
#%dir %{_sysconfdir}/sysconfig/
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
#%config(noreplace) %{_sysconfdir}/enduro-am-worker.toml
#%config(noreplace) %{_sysconfdir}/sysconfig/enduro-am-worker
#/var/lib/enduro/



%changelog server
* Wed May 19 2021 John Doe - 1.0-1
- First release
 
