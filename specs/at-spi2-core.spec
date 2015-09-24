%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           at-spi2-core
Version:        2.18.0
Release:        1%{?dist}
Summary:        Protocol definitions and daemon for D-Bus at-spi

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:        http://download.gnome.org/sources/at-spi2-core/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires:  freedesktop-sdk-base
BuildRequires:  dbus-dev
BuildRequires:  dbus-glib-dev
BuildRequires:  glib2-dev
BuildRequires:  gobject-introspection-dev
BuildRequires:  libXtst-dev
BuildRequires:  libXext-dev
BuildRequires:  libXi-dev

Requires:       dbus

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

%package dev
Summary: Development files and headers for at-spi2-core
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
The at-spi2-core-dev package includes the header files and
API documentation for libatspi.

%prep
%setup -q

%build
autoreconf -v --install --force
%configure --with-dbus-daemondir=/bin
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%{find_lang} %{name}

rm $RPM_BUILD_ROOT%{_libdir}/libatspi.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc COPYING AUTHORS README
%{_libexecdir}/at-spi2-registryd
%{_datadir}/dbus-1/accessibility-services/org.a11y.atspi.Registry.service
%{_sysconfdir}/at-spi2
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop
%{_libdir}/libatspi.so.*
%{_libdir}/girepository-1.0/Atspi-2.0.typelib
%{_libexecdir}/at-spi-bus-launcher
%{_datadir}/dbus-1/services/org.a11y.Bus.service


%files dev
%{_libdir}/libatspi.so
%{_datadir}/gtk-doc/html/libatspi
%{_datadir}/gir-1.0/Atspi-2.0.gir
%{_includedir}/at-spi-2.0
%{_libdir}/pkgconfig/atspi-2.pc

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 2.14.1-1
- Initial version based on F21
