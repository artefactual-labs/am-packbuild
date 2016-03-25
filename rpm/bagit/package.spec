Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: BagIt File Packager
Source: https://github.com/LibraryOfCongress/bagit-java/archive/v%{version}.zip
License: see /usr/share/doc/bagit/LICENSE.txt


%description
The BAGIT LIBRARY is a software library intended to support the creation, manipulation, and validation of bags.


%files
/usr/share/bagit
/usr/share/doc/bagit


%prep
rm -rf %{buildroot}/*
%setup -q


%install
gradle installApp

mkdir -p \
	%{buildroot}/usr/share/bagit/bin \
	%{buildroot}/usr/share/doc/bagit/ \
	%{buildroot}/usr/bin/

cp build/scripts/bagit %{buildroot}/usr/share/bagit/bin/bag

# Update APP_HOME PATH
sed -i 's/`pwd -P`/\/usr\/share\/bagit\//g' %{buildroot}/usr/share/bagit/bin/bag

cp -rf build/install/bagit/lib %{buildroot}/usr/share/bagit/
cp LICENSE.txt %{buildroot}/usr/share/doc/bagit/
cp README.md %{buildroot}/usr/share/doc/bagit/
