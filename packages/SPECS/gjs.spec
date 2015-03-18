%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:          gjs
Version:       1.43.3
Release:       1%{?dist}
Summary:       Javascript Bindings for GNOME

Group:         System Environment/Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:       MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:           http://live.gnome.org/Gjs/
#VCS:          git://git.gnome.org/gjs
Source0:       http://download.gnome.org/sources/gjs/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires: freedesktop-sdk-base
BuildRequires: mozjs24-dev
BuildRequires: cairo-gobject-dev
BuildRequires: gobject-introspection-dev
BuildRequires: dbus-glib-dev
BuildRequires: gtk3-dev
BuildRequires: gnome-common

Requires: gobject-introspection%{?_isa}

%description
Gjs allows using GNOME libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.

%package dev
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
Files for development with %{name}.

%prep
%setup -q

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; fi;
 %configure --disable-static)

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%check
#make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING NEWS README
%{_bindir}/gjs
%{_bindir}/gjs-console
%{_libdir}/*.so.*
%{_libdir}/gjs

%files dev
%doc examples/*
%{_includedir}/gjs-1.0
%{_libdir}/pkgconfig/gjs-1.0.pc
%{_libdir}/pkgconfig/gjs-internals-1.0.pc
%{_libdir}/*.so

%changelog
* Wed Nov 26 2014 Alexander Larsson <alexl@redhat.com> - 1.42.0-1
- Initial version, based on F21

