%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


Name: fixity
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Archivematica Storage Service
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual/fixity/
BuildRequires: python2-pip, python2-virtualenv
Requires: python2-pip
AutoReq: No
AutoProv: No
%description
fixity

%files
/usr/share/archivematica/virtualenvs/fixity/

%prep
rm -rf /usr/share/archivematica
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone \
  --quiet \
  --branch %{_branch} \
  --depth 1 \
  --single-branch \
  --recurse-submodules \
    https://github.com/artefactual/fixity \
    %{_sourcedir}/%{name}


%install
mkdir -p \
  %{buildroot}/usr/share/archivematica/virtualenvs/fixity/ 

virtualenv /usr/share/archivematica/virtualenvs/fixity
/usr/share/archivematica/virtualenvs/fixity/bin/pip install --upgrade pip
/usr/share/archivematica/virtualenvs/fixity/bin/pip install -r %{_sourcedir}/%{name}/requirements.txt
cd %{_sourcedir}/%{name} && /usr/share/archivematica/virtualenvs/fixity/bin/python setup.py install
virtualenv --relocatable /usr/share/archivematica/virtualenvs/fixity
cp -rf /usr/share/archivematica/virtualenvs/fixity/* %{buildroot}/usr/share/archivematica/virtualenvs/fixity/


%clean
rm -rf %{buildroot}


%post
ln -sf /usr/share/archivematica/virtualenvs/fixity/bin/fixity /usr/bin/fixity

%changelog
* Wed Jan 09 2019 - sysadmin@artefactual.com
- Create collectstatic directory in post script
* Tue Dec 11 2018 - sysadmin@artefactual.com
- Update collectstatic command: added --clear option
