Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: Temporal is a microservice orchestration platform which enables developers to build scalable applications without sacrificing productivity or reliability
URL: https://github.com/temporalio/temporal
Group: Application/SystemTools
License: MIT License
Source0: %{name}-%{version}.tar.gz

%description
Temporal is a microservice orchestration platform which enables developers to build scalable applications without sacrificing productivity or reliability. Temporal server executes units of application logic, Workflows, in a resilient manner that automatically handles intermittent failures, and retries failed operations.

%files
/usr/bin/temporal-cassandra-tool
/usr/bin/temporal-server
/usr/bin/temporal-sql-tool
/usr/share/temporal/schema/
%config /etc/temporal.yaml
%config /etc/systemd/system/temporal.service

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 0755 -d $RPM_BUILD_ROOT/etc/systemd/system/
install -m 0755 temporal-cassandra-tool $RPM_BUILD_ROOT/usr/bin/temporal-cassandra-tool
install -m 0755 temporal-server $RPM_BUILD_ROOT/usr/bin/temporal-server
install -m 0755 temporal-sql-tool $RPM_BUILD_ROOT/usr/bin/temporal-sql-tool
install -m 0644 temporal.yaml $RPM_BUILD_ROOT/etc/
install -m 0644 temporal.service $RPM_BUILD_ROOT/etc/systemd/system/
mkdir -p $RPM_BUILD_ROOT/usr/share/temporal/schema
cp -rf schema $RPM_BUILD_ROOT/usr/share/temporal/

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
