Name:          clutter
Version:       1.20.0
Release:       1%{?dist}
Summary:       Open Source software library for creating rich graphical user interfaces

Group:         Development/Libraries
License:       LGPLv2+
URL:           http://www.clutter-project.org/
Source0:       http://download.gnome.org/sources/clutter/1.20/clutter-%{version}.tar.xz

BuildRequires: gnome-sdk-base
BuildRequires: glib2-devel mesa-libGL-devel pango-devel
BuildRequires: cairo-gobject-devel gdk-pixbuf2-devel atk-devel
BuildRequires: cogl-devel
BuildRequires: gobject-introspection-devel >= 0.9.6
BuildRequires: gtk3-devel
BuildRequires: json-glib-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libXi-devel

Requires:      gobject-introspection

%description
Clutter is an open source software library for creating fast,
visually rich graphical user interfaces. The most obvious example
of potential usage is in media center type applications.
We hope however it can be used for a lot more.

%package devel
Summary:       Clutter development environment
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
clutter

%package       doc
Summary:       Documentation for %{name}
Group:         Documentation
Requires:      %{name} = %{version}-%{release}

%description   doc
Clutter is an open source software library for creating fast,
visually rich graphical user interfaces. The most obvious example
of potential usage is in media center type applications.
We hope however it can be used for a lot more.

This package contains documentation for clutter.

%prep
%setup -q

%build
%configure \
	--enable-xinput \
        --enable-gdk-backend

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -name '*.la' -delete

%find_lang clutter-1.0

%check
make check %{?_smp_mflags} V=1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f clutter-1.0.lang
%doc COPYING NEWS README
%{_libdir}/*.so.0
%{_libdir}/*.so.0.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir

%files doc
%{_datadir}/gtk-doc/html/clutter
%{_datadir}/gtk-doc/html/cally

%changelog
* Thu Dec 11 2014 Alexander Larsson <alexl@redhat.com> - 1.20.0-1
- Initial version
