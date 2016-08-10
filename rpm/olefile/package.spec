%define	pypackage	olefile
%define py_puresitedir  /usr/lib/python2.7/site-packages

Name:		python-%{pypackage}
Version:	0.43
Release:	1
Summary:	Python package to parse, read and write Microsoft OLE2 files 

Source0:	http://pypi.python.org/packages/source/o/olefile/olefile-%{version}.tar.gz
License:	BSD-2-Clause
BuildRoot:	{_tmppath}/%{name}-%{version}-buildroot
Group:		Development/Python
Url:		http://pypi.python.org/pypi/six/
BuildArch:	noarch
BuildRequires:  pkgconfig(python)

%description
olefile is a Python package to parse, read and write Microsoft OLE2 files (also called Structured Storage, Compound File Binary Format or Compound Document File Format), such as Microsoft Office 97-2003 documents, vbaProject.bin in MS Office 2007+ files, Image Composer and FlashPix files, Outlook messages, StickyNotes, several Microscopy file formats, McAfee antivirus quarantine files, etc.

%prep
%setup -n %{pypackage}-%{version}

%build
python setup.py build

%install
python setup.py install --root=%{buildroot} --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT
 
%files
%defattr(-,root,root)
%doc README.md
%{py_puresitedir}/*

%changelog

* Fri Jan 01 2016 dsilakov <denis.silakov@rosalab.ru> 1.10.0-1
- (1d3151d) Merge pull request #7 from import/python-six:auto_update
- (1d3151d) Updated to 1.10.0 (by updates_builder)


