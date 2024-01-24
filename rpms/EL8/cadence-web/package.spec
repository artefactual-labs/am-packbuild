Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: Cadence is a Fault-Oblivious Stateful Code Platform
URL: https://github.com/uber/cadence-web
Group: Application/SystemTools
License: MIT License
Source0: %{name}-%{version}.tar.gz

%description
Cadence is a distributed, scalable, durable, and highly available orchestration engine to execute asynchronous long-running business logic in a scalable and resilient way

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
cd %{_sourcedir}/%{name}-%{version} && npm install --unsafe-perm
#install -m 0755 -d $RPM_BUILD_ROOT/usr/local/share/cadence-web/
#install -m 0755 -d $RPM_BUILD_ROOT/etc/systemd/system/
mkdir -p $RPM_BUILD_ROOT/usr/share/cadence-web/
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system/

cp -rf %{_sourcedir}/%{name}-%{version}/* $RPM_BUILD_ROOT/usr/share/cadence-web/
cp %{_sourcedir}/cadence-web.service $RPM_BUILD_ROOT/etc/systemd/system/cadence-web.service


%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/share/cadence-web/
%config /etc/systemd/system/cadence-web.service


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
