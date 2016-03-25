Name:    %{name}
Version: %{version}
Release: 1%{?dist}
Summary: client, protocol, and server for running Java programs from CLI
Buildrequires: maven, gcc
Source: https://github.com/martylamb/nailgun/archive/master.zip
License: see /usr/share/doc/bagit-java/LICENSE.txt


%description
Nailgun is a client, protocol, and server for running Java programs from
the command line without incurring the JVM startup overhead. Programs run
in the server (which is implemented in Java), and are triggered by the
client (written in C), which handles all I/O.

%files
"/usr/bin/ng"
"/usr/share/doc/nailgun/README.md"
"/usr/share/doc/nailgun/LICENSE.txt"
"/usr/share/nailgun/"

%prep
rm -rf %{buildroot}/*
%setup -q -n nailgun-master

%install
make
mvn package

mkdir -p \
	%{buildroot}/usr/bin/ \
	%{buildroot}/usr/share/doc/nailgun/ \
	%{buildroot}/usr/share/nailgun/

cp ng  %{buildroot}/usr/bin/
cp LICENSE.txt README.md %{buildroot}/usr/share/doc/nailgun/
cp nailgun-server/target/*.jar %{buildroot}/usr/share/nailgun/


%changelog
