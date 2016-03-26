Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: JSTOR/Harvard Object Validation Environment
Buildrequires: maven, gcc
Source: https://github.com/openpreserve/jhove/archive/%{version}.zip
Patch: paths.patch
License: LGPL


%description
JHOVE (the JSTOR/Harvard Object Validation Environment, pronounced "jhove") is an extensible software framework for performing format identification, validation, and characterization of digital objects.


%files
/usr/share/jhove/
/usr/share/doc/jhove/
/usr/bin/jhove
/usr/bin/jhove-gui


%prep
rm -rf %{buildroot}/*
%setup -q
%patch


%install
mvn clean install

mkdir -p \
	%{buildroot}/usr/bin/ \
	%{buildroot}/usr/share/doc/jhove/ \
	%{buildroot}/usr/share/jhove/conf

cp jhove-installer/target/staging/scripts/jhove  %{buildroot}/usr/bin/
cp jhove-installer/target/staging/scripts/jhove-gui  %{buildroot}/usr/bin/
chmod 755 %{buildroot}/usr/bin/jhove %{buildroot}/usr/bin/jhove-gui

cp -rf jhove-installer/target/staging/config/*  %{buildroot}/usr/share/jhove/conf/
cp -rf jhove-installer/target/staging/bin %{buildroot}/usr/share/jhove/
cp -rf lib %{buildroot}/usr/share/jhove/

cp LICENSE README.md COPYING %{buildroot}/usr/share/doc/jhove/
