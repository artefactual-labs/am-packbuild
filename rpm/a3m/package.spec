%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%global _build_id_links alldebug

Name: a3m
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Lightweight Archivematica
Group: Application/System
License: AGPLv3
Source0: https://github.com/artefactual-labs/a3m/
Url: https://github.com/artefactual-labs/a3m
Vendor: Artefactual Systems Inc. <info@artefactual.com>
BuildRequires: python39-pip, python39, python3-virtualenv
Requires: python39-pip
AutoReq: No
AutoProv: No

%description
*a3m* is a lightweight version of Archivematica focused on AIP creation. It has
neither external dependencies, integration with access sytems, search
capabilities nor a graphical interface.

All functionality is made available as a `gRPC <https://grpc.io/docs/>`_ service
with a minimal set of methods and strongly typed messages. a3m can be executed
as a standalone process or be embedded as part of your application.

For more documentation, please see https://a3m.readthedocs.io.


%files
/usr/share/archivematica/virtualenvs/a3m/

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
    https://github.com/artefactual-labs/a3m \
    %{_sourcedir}/%{name}


%install
mkdir -p \
  %{buildroot}/usr/share/archivematica/virtualenvs/a3m/ 

virtualenv -p python3.9 /usr/share/archivematica/virtualenvs/a3m
/usr/share/archivematica/virtualenvs/a3m/bin/pip install --upgrade pip
/usr/share/archivematica/virtualenvs/a3m/bin/pip install -r %{_sourcedir}/%{name}/requirements.txt
cd %{_sourcedir}/%{name} && /usr/share/archivematica/virtualenvs/a3m/bin/python setup.py install
virtualenv --relocatable /usr/share/archivematica/virtualenvs/a3m
cp -rf /usr/share/archivematica/virtualenvs/a3m/* %{buildroot}/usr/share/archivematica/virtualenvs/a3m/

pathfix.py -ni /usr/bin/python3.9 %{buildroot}/usr/share/archivematica/virtualenvs/a3m/lib/python3.9/site-packages/sqlparse/cli.py
pathfix.py -ni /usr/bin/python3.9 %{buildroot}/usr/share/archivematica/virtualenvs/a3m/lib/python3.9/site-packages/django/bin/django-admin.py
pathfix.py -ni /usr/bin/python3.9 %{buildroot}/usr/share/archivematica/virtualenvs/a3m/lib/python3.9/site-packages/django/conf/project_template/manage.py-tpl
pathfix.py -ni /usr/bin/python3.9 %{buildroot}/usr/share/archivematica/virtualenvs/a3m/lib/python3.9/site-packages/google/protobuf/internal/_parameterized.py
pathfix.py -ni /usr/bin/python3.9 %{buildroot}/usr/share/archivematica/virtualenvs/a3m/*

%clean
rm -rf %{buildroot}


%post
ln -sf /usr/share/archivematica/virtualenvs/a3m/bin/a3m /usr/bin/a3m
ln -sf /usr/share/archivematica/virtualenvs/a3m/bin/a3md /usr/bin/a3md
pathfix.py -pni '/usr/share/archivematica/virtualenvs/a3m/bin/python3.9' /usr/share/archivematica/virtualenvs/a3m/bin/a3m
pathfix.py -pni '/usr/share/archivematica/virtualenvs/a3m/bin/python3.9' /usr/share/archivematica/virtualenvs/a3m/bin/a3md


%changelog
* Tue Sep 05 2022 - sysadmin@artefactual.com
- Create initial a3m package
