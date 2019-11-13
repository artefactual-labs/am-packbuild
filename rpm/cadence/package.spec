Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: Cadence is a Fault-Oblivious Stateful Code Platform
URL: https://github.com/uber/cadence
Group: Application/SystemTools
License: MIT License
Source0: %{name}-%{version}.tar.gz

%description
Cadence is a distributed, scalable, durable, and highly available orchestration engine to execute asynchronous long-running business logic in a scalable and resilient way

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 0755 -d $RPM_BUILD_ROOT/etc/systemd/system/
install -m 0755 cadence $RPM_BUILD_ROOT/usr/bin/cadence
install -m 0755 cadence-server $RPM_BUILD_ROOT/usr/bin/cadence-server
install -m 0755 cadence-sql-tool $RPM_BUILD_ROOT/usr/bin/cadence-sql-tool
install -m 0644 cadence.yaml $RPM_BUILD_ROOT/etc/
install -m 0644 cadence.service $RPM_BUILD_ROOT/etc/systemd/system/
%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/cadence
/usr/bin/cadence-server
/usr/bin/cadence-sql-tool
%config /etc/cadence.yaml
%config /etc/systemd/system/cadence.service


%post

# Create enduro user and group
getent group enduro >/dev/null || groupadd -f -g 444 -r enduro
if ! getent passwd enduro >/dev/null ; then
  if ! getent passwd 444 >/dev/null ; then
    useradd -r -u 444 -g enduro -d /var/lib/enduro/ -s /sbin/nologin -c "Enduro system account" -m enduro
    else
    useradd -r -g enduro -d /var/lib/enduro/ -s /sbin/nologin -c "Enduro system account" -m enduro
  fi
fi

systemctl daemon-reload
