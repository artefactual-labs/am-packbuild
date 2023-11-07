Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: The Temporal Web UI provides users with Workflow Execution state and metadata for debugging purposes.
URL: https://github.com/temporalio/ui-server
Group: Application/SystemTools
License: MIT License
Source0: %{name}-%{version}.tar.gz

%description
The Temporal Web UI provides users with Workflow Execution state and metadata for debugging purposes.

%files
/usr/bin/temporal-ui
%config(noreplace) /etc/temporal-ui/config/temporal.yml
%config(noreplace) /etc/systemd/system/temporal-ui.service

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 0755 -d $RPM_BUILD_ROOT/etc/systemd/system/
install -m 0755 -d $RPM_BUILD_ROOT/etc/temporal-ui/config/
install -m 0755 temporal-ui $RPM_BUILD_ROOT/usr/bin/temporal-ui
install -m 0644 temporal-ui.conf.yml $RPM_BUILD_ROOT/etc/temporal-ui/config/temporal.yml
install -m 0644 temporal-ui.service $RPM_BUILD_ROOT/etc/systemd/system/temporal-ui.service

%clean
rm -rf $RPM_BUILD_ROOT

%post

# Create temporal user and group
getent group temporal >/dev/null || groupadd -f -g 445 -r temporal
if ! getent passwd temporal >/dev/null ; then
  if ! getent passwd 445 >/dev/null ; then
    useradd -r -u 445 -g temporal -d /var/lib/temporal/ -s /sbin/nologin -c "Temporal system account" -m temporal
    else
    useradd -r -g temporal -d /var/lib/temporal/ -s /sbin/nologin -c "Temporal system account" -m temporal
  fi
fi

systemctl daemon-reload
