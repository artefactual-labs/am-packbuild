%define aname %{name}
Name: %{aname}
Version: %{version}
Release: 1%{?dist}
Summary: Automatic certificate acquisition tool
License: MIT
URL: https://github.com/hlandau/acme
Group: Applications/System
Requires: libcap
Conflicts: %{aname}-nocgo
%ifarch i386 i686
%define goarch 386_cgo
%else
%ifarch x86_64
%define goarch amd64_cgo
%else
%ifarch ppc64le
%define goarch ppc64le_cgo
%else
%define goarch ERROR
%endif
%endif
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
Source: %{aname}_%{version}.orig.tar.gz

%define debug_package %{nil}

%description
Automatic certificate acquisition tool for ACME servers such as Let's Encrypt.

%prep
#%setup -n %{aname}_%{version}/%{aname}-v%{version}-linux_%{goarch}
%setup -q

%build
make BUILDFLAGS="-ldflags \"-X github.com/hlandau/buildinfo.RawBuildInfo=$(echo -n 'acmetool CentOS version %{version}' | base64)\""
mkdir -p usr/share/man/man8
bin/acmetool --help-man > usr/share/man/man8/acmetool.8
gzip usr/share/man/man8/acmetool.8

%install
install -Dm0755 bin/acmetool $RPM_BUILD_ROOT/usr/bin/acmetool
install -Dm0644 usr/share/man/man8/acmetool.8.gz $RPM_BUILD_ROOT/usr/share/man/man8/acmetool.8.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(755,root,root) %{_bindir}/acmetool
%attr(644,root,root) %{_mandir}/man8/acmetool.8.gz
