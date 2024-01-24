%global _default_patch_fuzz 2
Name: %{name}
Version: %{version}
Release: 4%{?dist}
Summary: File Information Tool Set (FITS)
Buildrequires: ant, gcc
Source: https://github.com/harvard-lts/fits/archive/v%{version}.zip
Patch: fits-home.patch
Patch1: fits-log4j.patch
Patch2: fits-enable-toolOutput.patch
Patch3: fits-use-system-exitftool.patch
Patch4: fits-disable-mediainfo.patch
Patch5: fits-ngserver-logging-and-maxmem.patch
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
%config /etc/sysconfig/fits

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
	%{buildroot}/etc/sysconfig\
	%{buildroot}/usr/lib/systemd/system

cp fits.sh fits-ngserver.sh fits-env.sh  %{buildroot}/usr/bin/
cp -rf lib/* %{buildroot}/usr/share/fits/lib/
cp lib-fits/fits-%{version}.jar %{buildroot}/usr/share/fits/lib/
cp -rf xml %{buildroot}/usr/share/fits/
cp log4j.properties version.properties %{buildroot}/usr/share/fits/
cp %{_sourcedir}/fits-nailgun.service %{buildroot}/usr/lib/systemd/system/fits-nailgun.service
cp -rf tools/ffident  %{buildroot}/usr/share/fits/tools/
cp -rf tools/droid  %{buildroot}/usr/share/fits/tools/
cp -rf %{_etcdir}/sysconfig/fits  %{buildroot}/etc/sysconfig/fits


%post
touch /var/log/archivematica/fits.log
chown archivematica.archivematica /var/log/archivematica/fits.log
systemctl daemon-reload
if systemctl is-enabled --quiet fits-nailgun.service ; then
	systemctl restart fits-nailgun.service
fi

%preun
if [ $1 == 0 ]; then #uninstall
  systemctl unmask fits-nailgun.service
  systemctl stop fits-nailgun.service
  systemctl disable fits-nailgun.service
fi

%postun
if [ $1 == 0 ]; then #uninstall
  systemctl daemon-reload
  systemctl reset-failed
fi

%changelog
* Fri Dec 06 2019 sysadmin@artefactual.com
- Only restart service if it's enabled
* Tue Nov 19 2019 - sysadmin@artefactual.com
- Make JVM heap size configurable /etc/sysconfig/fits
- Fix systemd starting & stopping the service on install & uninstall
* Tue Oct 30 2018 - sysadmin@artefactual.com
- Update systemd init script to use nailgun-server-latest-SNAPSHOT.jar
  symlink
