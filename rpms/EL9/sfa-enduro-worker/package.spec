%define _builddir ./
%define build_timestamp %(date +"%Y%m%d%H%M")

Name: sfa-enduro-worker
Summary: A tool designed to run custom SFA workflows
Version: %{version} 
Release: %{build_timestamp}%{?dist}
License: ASL 2.0

# BuildRequires: golang
BuildRequires: systemd-rpm-macros

Provides: %{name} = %{version}
%description
SFA Enduro worker

%global debug_package %{nil}


%build
hack/build_dist.sh -o sfa-enduro-worker ./cmd/worker/


%install 
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 644 %{name}.toml %{buildroot}%{_sysconfdir}/%{name}.toml


%check
# go test should be here... :)

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service


%files
%dir %{_sysconfdir}
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
#%config(noreplace) %{_etcdir}/%{name}.toml
%config(noreplace) %{_sysconfdir}/%{name}.toml



%changelog
* Wed May 19 2021 John Doe - 1.0-1
- First release
 
