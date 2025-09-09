Name: bulk_extractor
Version: 2.1.1
Release: 1%{?dist}
Summary: A forensic media scanning and analysis tool
Source: https://github.com/simsong/bulk_extractor/releases/download/v%{version}/bulk_extractor-%{version}.tar.gz
License: MIT and Public Domain
URL: https://github.com/simsong/bulk_extractor

# Avoid auto-requiring system libewf/re2 since we vendor them.
%global __requires_exclude ^lib(ewf|re2|absl_.*)\\.so.*$

%description
bulk_extractor is a C++ program that scans a disk image, a file, or a
directory of files and extracts useful information without parsing the
file system or file system structures. The results are stored in feature files
that can be easily inspected, parsed, or processed with automated tools.
It also creates histograms of features that it finds, as features that are
more common tend to be more important.

%prep
%autosetup -p1 -n bulk_extractor-%{version}
# Enforce C++17 across generated makefiles to avoid -std=c++11 overriding.
find . -name 'Makefile.in' -print0 | xargs -0 sed -i 's/-std=c++11/-std=gnu++17/g'

%build
# Force C++17 and chrono literals; ensure filesystem links on GCC 8 via LIBS.
%configure \
    CXXFLAGS="%{optflags} -std=gnu++17 -fext-numeric-literals" \
    LIBS="$LIBS -lstdc++fs"
%make_build

%install
%make_install

# Bundle required shared libraries to avoid external runtime deps.
mkdir -p %{buildroot}%{_libdir}/bulk_extractor
# libewf from the toolchain we built in the Docker image
if [ -e /usr/local/lib64/libewf.so ] || ls /usr/local/lib64/libewf.so.* >/dev/null 2>&1; then \
  cp -a /usr/local/lib64/libewf.so* %{buildroot}%{_libdir}/bulk_extractor/ ; \
elif [ -e /usr/local/lib/libewf.so ] || ls /usr/local/lib/libewf.so.* >/dev/null 2>&1; then \
  cp -a /usr/local/lib/libewf.so* %{buildroot}%{_libdir}/bulk_extractor/ ; \
fi
# libre2 from the system (EL8)
for d in /usr/lib64 /usr/local/lib64 /usr/lib /usr/local/lib; do \
  if ls $d/libre2.so* >/dev/null 2>&1; then \
    cp -a $d/libre2.so* %{buildroot}%{_libdir}/bulk_extractor/ ; \
    break; \
  fi; \
done
# Bundle abseil libs if libre2 depends on them
for d in /usr/lib64 /usr/local/lib64 /usr/lib /usr/local/lib; do \
  if ls $d/libabsl_*.so* >/dev/null 2>&1; then \
    cp -a $d/libabsl_*.so* %{buildroot}%{_libdir}/bulk_extractor/ ; \
    break; \
  fi; \
done
# Ensure the expected SONAME symlink exists (libre2.so.0 on EL8)
if [ ! -e %{buildroot}%{_libdir}/bulk_extractor/libre2.so.0 ] && ls %{buildroot}%{_libdir}/bulk_extractor/libre2.so.* >/dev/null 2>&1; then \
  tgt=$(basename $(ls -1 %{buildroot}%{_libdir}/bulk_extractor/libre2.so.* | head -n1)); \
  ln -s "$tgt" %{buildroot}%{_libdir}/bulk_extractor/libre2.so.0 || true; \
fi

# Ensure the binary prefers the bundled libs via RUNPATH.
# Install a wrapper to set LD_LIBRARY_PATH so we don't rely on RUNPATH.
mkdir -p %{buildroot}%{_libexecdir}/bulk_extractor
mv %{buildroot}%{_bindir}/bulk_extractor %{buildroot}%{_libexecdir}/bulk_extractor/bulk_extractor.real
cat > %{buildroot}%{_bindir}/bulk_extractor << 'EOF'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
LIB64="$HERE/../lib64/bulk_extractor"
LIB32="$HERE/../lib/bulk_extractor"
if [ -d "$LIB64" ] || [ -d "$LIB32" ]; then
  if [ -z "$LD_LIBRARY_PATH" ]; then
    export LD_LIBRARY_PATH="$LIB64:$LIB32"
  else
    export LD_LIBRARY_PATH="$LIB64:$LIB32:$LD_LIBRARY_PATH"
  fi
fi
exec "$HERE/../libexec/bulk_extractor/bulk_extractor.real" "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/bulk_extractor

%files
%license LICENSE.md
%doc ChangeLog README.md NEWS COPYING
%doc doc/*.{html,md,txt} doc/Diagnostic_Notes/*.{md,html}
%{_bindir}/bulk_extractor
%{_libexecdir}/bulk_extractor/bulk_extractor.real
%{_libdir}/bulk_extractor/libewf.so*
%{_libdir}/bulk_extractor/libre2.so*
%{_libdir}/bulk_extractor/libabsl_*.so*
%{_mandir}/man1/bulk_extractor.1*
