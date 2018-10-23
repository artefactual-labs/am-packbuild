%global _default_patch_fuzz 2
Name: %{name}
Version: %{version}
Release: 2%{?dist}
Summary: File Information Tool Set (FITS)
Buildrequires: ant, gcc
Source: https://github.com/harvard-lts/fits/archive/v%{version}.zip
Patch: fits-home.patch
Patch1: fits-log4j.patch
Patch2: fits-enable-toolOutput.patch
Patch3: fits-use-system-exitftool.patch
Patch4: fits-disable-mediainfo.patch
Patch5: fits-ngserver-logging.patch
Patch6: fits-logging.patch
Requires: mediainfo, libzen, perl-Image-ExifTool, nailgun
License: GPLv3


%description
The File Information Tool Set (FITS) identifies, validates, and extracts technical metadata for various file formats. It wraps several third-party open source tools, normalizes and consolidates their output, and reports any errors.


%files
/usr/bin/fits.sh
/usr/bin/fits-ngserver.sh
/usr/bin/fits-env.sh
/usr/share/fits
/usr/lib/systemd/system/fits-nailgun.service


%prep
rm -rf %{buildroot}/*
%setup
%patch
%patch1
%patch2
%patch3
%patch4
%patch5
%patch6

%install
ANT_OPTS=-Dfile.encoding=UTF8 ant clean-compile-jar
mkdir -p \
	%{buildroot}/usr/bin/ \
	%{buildroot}/usr/share/fits/lib \
	%{buildroot}/usr/share/fits/tools \
	%{buildroot}/usr/lib/systemd/system

cp fits.sh fits-ngserver.sh fits-env.sh  %{buildroot}/usr/bin/
cp -rf lib/* %{buildroot}/usr/share/fits/lib/
cp lib-fits/fits-%{version}.jar %{buildroot}/usr/share/fits/lib/
cp -rf xml %{buildroot}/usr/share/fits/
cp log4j.properties version.properties %{buildroot}/usr/share/fits/
cp %{_sourcedir}/fits-nailgun.service %{buildroot}/usr/lib/systemd/system/fits-nailgun.service
cp -rf tools/ffident  %{buildroot}/usr/share/fits/tools/
cp -rf tools/droid  %{buildroot}/usr/share/fits/tools/


%post
touch /var/log/archivematica/fits.log
chown archivematica.archivematica /var/log/archivematica/fits.log
# TODO: reload only when the script changes. Check https://fedoraproject.org/wiki/Packaging:Scriptlets?rd=Packaging:ScriptletSnippets#Systemd
systemctl daemon-reload
