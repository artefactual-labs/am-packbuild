%define _builddir ./
%define build_timestamp %(date +"%Y%m%d%H%M")
%define dips_name sfa-dips

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
SFA Enduro worker

%global debug_package %{nil}

%package -n %{dips_name}
Summary: SFA DIPs application

%description -n %{dips_name}
SFA DIPs API server and Temporal worker


%build
hack/build_dist.sh -o sfa-enduro-worker ./cmd/worker/
hack/build_dist.sh -o sfa-dips ./cmd/sfa-dips/


%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0755 %{dips_name} %{buildroot}%{_bindir}/%{dips_name}
install -Dpm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 644 %{dips_name}.service %{buildroot}%{_unitdir}/%{dips_name}.service
install -Dpm 644 %{name}.toml %{buildroot}%{_sysconfdir}/%{name}.toml
install -Dpm 644 %{dips_name}.toml %{buildroot}%{_sysconfdir}/%{dips_name}.toml

%check
# go test should be here... :)

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%post -n %{dips_name}
%systemd_post %{dips_name}.service

%preun -n %{dips_name}
%systemd_preun %{dips_name}.service


%files
%dir %{_sysconfdir}
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
#%config(noreplace) %{_etcdir}/%{name}.toml
%config(noreplace) %{_sysconfdir}/%{name}.toml

%files -n %{dips_name}
%dir %{_sysconfdir}
%{_bindir}/%{dips_name}
%{_unitdir}/%{dips_name}.service
%config(noreplace) %{_sysconfdir}/%{dips_name}.toml


%changelog
* Wed May 19 2021 John Doe - 1.0-1
- First release
