Name: archivematica-devtools
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Developer tools for Archivematica
Source: https://github.com/artefactual/archivematica-devtools
Patch: upgrade-centos-paths.patch
License: AGPLv3


%description
This package contains a set of developer tools intended to help administrate
 an installation of Archivematica. They can also be useful for systems
 administrators in controlling production Archivematica installations.


%files
/usr/lib/archivematica/devtools
/usr/bin/am


%prep
rm -rf %{_sourcedir}/archivematica-devtools
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone \
  --quiet \
  --branch %{branch} \
  --depth 1 \
  --single-branch \
  --recurse-submodules \
   https://github.com/artefactual/archivematica-devtools \
    %{_sourcedir}/%{name}

cd %{_sourcedir}/%{name} && patch -p1 < ../upgrade-centos-paths.patch

%install

mkdir -p \
	%{buildroot}/usr/lib/archivematica/devtools/ \
	%{buildroot}/usr/bin/


cp -rf %{_sourcedir}/%{name}/tools/* %{buildroot}/usr/lib/archivematica/devtools/
cp -rf %{_sourcedir}/%{name}/bin/am %{buildroot}/usr/bin/am
