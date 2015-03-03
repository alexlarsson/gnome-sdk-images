Name: pygobject3
Version: 3.14.0
Release: 1%{?dist}
License: LGPLv2+ and MIT
Group: Development/Languages
Summary: Python 3 bindings for GObject Introspection
URL: https://live.gnome.org/PyGObject
#VCS: git:git://git.gnome.org/pygobject
Source: http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.14/pygobject-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: glib2-dev
BuildRequires: gobject-introspection-dev
BuildRequires: python3-cairo-dev
BuildRequires: cairo-gobject-dev

# The cairo override module depends on this
Requires: python3-cairo

%description
The %{name} package provides a convenient wrapper for the GObject library
for use in Python3 programs.

%package dev
Summary: Development files for embedding PyGObject introspection support
Group: Development/Languages
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gobject-introspection-dev%{?_isa}

%description dev
This package contains files required to embed PyGObject

%prep
%setup -q -n pygobject-%{version}

find -name '*.py' | xargs sed -i '1s|^#!python|#!/usr/bin/python3|'

%build
export PYTHON=python3

%configure
make %{?_smp_mflags} V=1

%install
make DESTDIR=$RPM_BUILD_ROOT install V=1
find $RPM_BUILD_ROOT -name '*.la' -delete
find $RPM_BUILD_ROOT -name '*.a' -delete

# Don't include makefiles in the installed docs, in order to avoid creating
# multilib conflicts
rm -rf _docs
mkdir _docs
cp -a examples _docs
rm _docs/examples/Makefile*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644, root, root, 755)
%doc AUTHORS NEWS README COPYING
%dir %{_libdir}/python3.*/site-packages/gi
%{_libdir}/python3.*/site-packages/gi/*
%{_libdir}/python3.*/site-packages/pygobject-*.egg-info
%{_libdir}/python3.*/site-packages/pygtkcompat/

%files dev
%defattr(644, root, root, 755)
%doc _docs/*
%dir %{_includedir}/pygobject-3.0/
%{_includedir}/pygobject-3.0/pygobject.h
%{_libdir}/pkgconfig/pygobject-3.0.pc

%changelog
* Tue Feb  3 2015 Alexander Larsson <alexl@redhat.com> - 3.14.0-1
- initial version
