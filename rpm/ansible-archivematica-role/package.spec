%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


Name: archivematica-ansible-roles
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Archivematica ansible roles
Group: Application/System
License: AGPLv3
BuildRequires: git, ansible
Requires: git, ansible
AutoReq: No
AutoProv: No
%description
Archivematica ansible roles needed for deployment

%files
/etc/ansible/roles/

%prep
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/etc/ansible/roles/

git clone \
  --quiet \
  --branch %{_branch} \
  --depth 1 \
  --single-branch \
  --recurse-submodules \
    https://github.com/artefactual/deploy-pub \
    %{_sourcedir}/%{name}

%install
mkdir -p \
  %{buildroot}/etc/ansible/roles/ 

ansible-galaxy install -f -p %{buildroot}/etc/ansible/roles/ -r %{_sourcedir}/%{name}/playbooks/archivematica-centos7/requirements.yml


%clean
rm -rf %{buildroot}


%changelog
* Tue Dec 03 2019 - sysadmin@artefactual.com
- Initial work
