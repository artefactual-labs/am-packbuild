
Summary: Format Identification for Digital Objects (FIDO).
Name: fido
Version: %{rpmversion}
Release: %{rpmrelease}
Source0: %{name}-%{rpmversion}-%{rpmrelease}.tar.gz
License: Apache License 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{rpmversion}-%{rpmrelease}-buildroot
BuildArch: noarch
BuildRequires: python-virtualenv
Requires: python-six, python-olefile
Url: http://openpreservation.org/technology/products/%{name}/

%description
A command-line tool to identify the file formats of digital objects. FIDO uses the UK National Archives (TNA) PRONOM File Format and Container descriptions.

%prep
%setup -n %{name}-%{rpmversion}-%{rpmrelease} -n %{name}-%{rpmversion}-%{rpmrelease}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES bdist_rpm

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
