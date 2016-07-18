
Summary: Format Identification for Digital Objects (FIDO).
Name: fido
Version: 1.3.4
Release: 84
Source0: %{name}-%{version}-84.tar.gz
License: Apache License 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-84-buildroot
BuildArch: noarch
BuildRequires: python-virtualenv
Requires: python-six, python-olefile
Url: http://openpreservation.org/technology/products/%{name}/

%description
A command-line tool to identify the file formats of digital objects. FIDO uses the UK National Archives (TNA) PRONOM File Format and Container descriptions.

%prep
%setup -n %{name}-%{version}-84 -n %{name}-1.3.4-84

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
