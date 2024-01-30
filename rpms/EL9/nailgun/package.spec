Name:    %{name}
Version: %{version}
Release: 1%{?dist}
Summary: client, protocol, and server for running Java programs from CLI
Buildrequires: maven, gcc, java-devel, javapackages-tools, java-headless
Source: https://github.com/facebook/nailgun/archive/nailgun-all-0.9.3.zip
License: Apache License 2.0
Patch: change-client-name.patch
Patch1: makefile-change-client-name.patch

%description
Nailgun is a client, protocol, and server for running Java programs from
the command line without incurring the JVM startup overhead. Programs run
in the server (which is implemented in Java), and are triggered by the
client (written in C), which handles all I/O.

%files
"/usr/bin/ng-nailgun"
"/usr/share/doc/nailgun/README.md"
"/usr/share/doc/nailgun/LICENSE.txt"
"/usr/share/nailgun/"

%prep
rm -rf %{buildroot}/*
%setup -q -n nailgun-nailgun-all-0.9.3

%patch
%patch1

%install
make ng
mvn package

mkdir -p \
	%{buildroot}/usr/bin/ \
	%{buildroot}/usr/share/doc/nailgun/ \
	%{buildroot}/usr/share/nailgun/

cp ng-nailgun  %{buildroot}/usr/bin/
cp LICENSE.txt README.md %{buildroot}/usr/share/doc/nailgun/
cp nailgun-server/target/*.jar %{buildroot}/usr/share/nailgun/

%post
ln -s -f /usr/share/nailgun/nailgun-server-0.9.3-SNAPSHOT.jar /usr/share/nailgun/nailgun-server-latest-SNAPSHOT.jar

%postun
rm -f /usr/share/nailgun/nailgun-server-latest-SNAPSHOT.jar

%changelog
* Mon Oct 29 2018 - sysadmin@artefactual.com
- bump version to 0.9.3
- use ng-nailgun client name instead of ng
- add nailgun-server-latest-SNAPSHOT.jar symlink
