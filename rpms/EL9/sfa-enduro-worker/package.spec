%define _builddir ./
%define build_timestamp %(date +"%Y%m%d%H%M")
%define dips_name sfa-dips-worker

Name: sfa-enduro-worker
Summary: A tool designed to run custom SFA workflows
Version: %{version}
Release: %{build_timestamp}%{?dist}
License: ASL 2.0
Obsoletes: preprocessing-worker <= 1.0.0

# BuildRequires: golang
BuildRequires: systemd-rpm-macros

Provides: %{name} = %{version}
%description
SFA Enduro workers

%global debug_package %{nil}


%build
hack/build_dist.sh -o sfa-enduro-worker ./cmd/worker/
hack/build_dist.sh -o sfa-dips-worker ./cmd/sfa-dips/


%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0755 %{dips_name} %{buildroot}%{_bindir}/%{dips_name}
install -Dpm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 644 %{dips_name}.service %{buildroot}%{_unitdir}/%{dips_name}.service
install -Dpm 644 %{name}.toml %{buildroot}%{_sysconfdir}/%{name}.toml


%check
# go test should be here... :)

%post
%systemd_post %{name}.service
%systemd_post %{dips_name}.service

%preun
%systemd_preun %{name}.service
%systemd_preun %{dips_name}.service


%files
%dir %{_sysconfdir}
%{_bindir}/%{name}
%{_bindir}/%{dips_name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{dips_name}.service
#%config(noreplace) %{_etcdir}/%{name}.toml
%config(noreplace) %{_sysconfdir}/%{name}.toml



%changelog
* Wed May 19 2021 John Doe - 1.0-1
- First release
