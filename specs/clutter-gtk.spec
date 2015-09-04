%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

%define         clutter_version 1.0

Name:           clutter-gtk
Version:        1.6.2
Release:        1%{?dist}
Summary:        A basic GTK clutter widget

Group:          Development/Languages
License:        LGPLv2+
URL:            http://www.clutter-project.org
Source0:        http://download.gnome.org/sources/clutter-gtk/%{release_version}/clutter-gtk-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: gtk3-dev
BuildRequires: clutter-dev
BuildRequires: gobject-introspection-dev

%description
clutter-gtk is a library which allows the embedding of a Clutter
canvas (or "stage") into a GTK+ application, as well as embedding
GTK+ widgets inside the stage.

%package dev
Summary:        Clutter-gtk development environment
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description dev
Header files and libraries for building a extension library for the
clutter-gtk.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete

%find_lang cluttergtk-1.0

%check
make check %{?_smp_mflags} V=1


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f cluttergtk-1.0.lang
%doc COPYING NEWS
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkClutter-%{clutter_version}.typelib

%files dev
%{_includedir}/clutter-gtk-%{clutter_version}/
%{_libdir}/pkgconfig/clutter-gtk-%{clutter_version}.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkClutter-%{clutter_version}.gir
%{_datadir}/gtk-doc/html/clutter-gtk-1.0

%changelog
* Thu Dec 11 2014 Alexander Larsson <alexl@redhat.com> - 1.6.0-1
- Initial version
