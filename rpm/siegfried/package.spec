Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: Siegfried is a signature-based file format identification tool.
URL: http://www.itforarchivists.com/siegfried
Group: Application/SystemTools
License: Apache License, Version 2.0
Source0: %{name}-%{version}.tar.gz

%description
Siegfried is a signature-based file format identification tool.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 0755 roy $RPM_BUILD_ROOT/usr/bin/roy
install -m 0755 sf $RPM_BUILD_ROOT/usr/bin/sf
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/siegfried
cp -r /go/src/github.com/richardlehane/siegfried/cmd/roy/data/* $RPM_BUILD_ROOT/usr/share/siegfried/

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/roy
/usr/bin/sf
/usr/share/siegfried/

%post
userID=`id -u archivematica 2>/dev/null`
if [ "${userID}" != 333 ]; then
  useradd --uid 333 --user-group --home /var/lib/archivematica archivematica
fi
chown -R archivematica:archivematica /usr/share/siegfried
