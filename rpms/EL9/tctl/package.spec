Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: The Temporal CLI is a command-line tool you can use to perform various tasks on a Temporal Server.
URL: https://github.com/temporalio/tctl
Group: Application/SystemTools
License: MIT License
Source0: %{name}-%{version}.tar.gz

%description
The Temporal CLI is a command-line tool you can use to perform various tasks on a Temporal Server. It can perform namespace operations such as register, update, and describe as well as Workflow operations like start Workflow, show Workflow history, and signal Workflow

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 0755 -d $RPM_BUILD_ROOT/etc/systemd/system/
install -m 0755 tctl $RPM_BUILD_ROOT/usr/bin/tctl
install -m 0755 tctl-authorization-plugin $RPM_BUILD_ROOT/usr/bin/tctl-authorization-plugin

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/tctl
/usr/bin/tctl-authorization-plugin


%post
