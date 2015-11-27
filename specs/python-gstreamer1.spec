Name:           python-gstreamer1
Version:        1.6.1
Release:        1%{?dist}
Summary:        Python bindings for GStreamer

Group:          Development/Languages
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-python/gst-python-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
Requires:       pygobject3%{?_isa}
Requires:       gstreamer1%{?_isa}

BuildRequires:  gstreamer1-dev
BuildRequires:  pygobject3-dev
BuildRequires:  python3-cairo-dev

%description
This module contains PyGObject overrides to make it easier to write
applications that use GStreamer 1.x in Python 3.

%prep
%setup -q -n gst-python-%{version}

find -name '*.py' | xargs sed -i '1s|^#!python|#!python3|'

%build
%configure PYTHON=python3
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/python3.*/site-packages/gi/overrides/*
%{_libdir}/gstreamer-1.0/libgstpythonplugin.*.so

%changelog
* Fri Nov 27 2015 Alexander Larsson <alexl@redhat.com> - 1.6.1-1
- initial version
