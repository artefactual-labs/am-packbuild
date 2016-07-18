%define	pypackage	six
%define py_puresitedir  /usr/lib/python2.7/site-packages

Name:		python-%{pypackage}
Version:	1.10.0
Release:	1
Summary:	Python 2 and 3 compatibility utilities

Source0:	http://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz
License:	MIT
BuildRoot:	{_tmppath}/%{name}-%{version}-buildroot
Group:		Development/Python
Url:		http://pypi.python.org/pypi/six/
BuildArch:	noarch
BuildRequires:  pkgconfig(python)

%description
Six is a Python 2 and 3 compatibility library.  It provides utility functions
for smoothing over the differences between the Python versions with the goal of
writing Python code that is compatible on both Python versions.  See the
documentation for more information on what is provided.

Six supports Python 2.4+.

Online documentation is at http://packages.python.org/six/.

Bugs can be reported to http://bitbucket.org/gutworth/six.  The code can also
be found there.

%prep
%setup -n %{pypackage}-%{version}

%build
chmod 644 README
python setup.py build

%install
python setup.py install --root=%{buildroot} --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT
 
%files
%defattr(-,root,root)
%doc LICENSE README documentation/index.rst
%{py_puresitedir}/*

%changelog

* Fri Jan 01 2016 dsilakov <denis.silakov@rosalab.ru> 1.10.0-1
- (1d3151d) Merge pull request #7 from import/python-six:auto_update
- (1d3151d) Updated to 1.10.0 (by updates_builder)


