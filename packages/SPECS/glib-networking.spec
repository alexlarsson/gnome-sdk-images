%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           glib-networking
Version:        2.43.92
Release:        1%{?dist}
Summary:        Networking support for GLib

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.gnome.org
Source:         http://download.gnome.org/sources/glib-networking/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires:  freedesktop-sdk-base
BuildRequires:  glib2-dev
BuildRequires:  libproxy-dev
BuildRequires:  gsettings-desktop-schemas-dev

Requires:       ca-certificates
Requires:       glib2
Requires:       gsettings-desktop-schemas

%description
This package contains modules that extend the networking support in
GIO. In particular, it contains libproxy- and GSettings-based
GProxyResolver implementations and a gnutls-based GTlsConnection
implementation.

%prep
%setup -q


%build
%configure --disable-static --with-libproxy

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la

%find_lang %{name}

%post
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules

%postun
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules

%files -f %{name}.lang
%doc COPYING NEWS README
%{_libdir}/gio/modules/libgiolibproxy.so
%{_libdir}/gio/modules/libgiognomeproxy.so
%{_libdir}/gio/modules/libgiognutls.so
%{_libexecdir}/glib-pacrunner
%{_datadir}/dbus-1/services/org.gtk.GLib.PACRunner.service

%changelog
* Mon Nov 24 2014 Alexander Larsson <alexl@redhat.com> - 2.42.0-1
- Initial version, based on F21
