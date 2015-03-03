%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           dconf
Version:        0.23.1
Release:        1%{?dist}
Summary:        A configuration system

Group:          System Environment/Base
License:        LGPLv2+ and GPLv2+ and GPLv3+
URL:            http://live.gnome.org/dconf
#VCS:           git:git://git.gnome.org/dconf
Source0:        http://download.gnome.org/sources/dconf/%{release_version}/dconf-%{version}.tar.xz

BuildRequires:  glib2-dev
BuildRequires:  dbus-dev
BuildRequires:  vala-dev

Requires:       glib2

%description
dconf is a low-level configuration system. Its main purpose is to provide a
backend to the GSettings API in GLib.

%package dev
Summary: Header files and libraries for dconf development
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description dev
dconf development package. Contains files needed for doing software
development using dconf.

%prep
%setup -q

%build
%configure --disable-static --disable-man
make V=1 %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
#we need this beacuse ibus and gdm installs file there
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dconf/db
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dconf/profile

%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files
%doc COPYING
%dir %{_sysconfdir}/dconf
%dir %{_sysconfdir}/dconf/db
%dir %{_sysconfdir}/dconf/profile
%{_libdir}/gio/modules/libdconfsettings.so
%{_libexecdir}/dconf-service
%{_datadir}/dbus-1/services/ca.desrt.dconf.service
%{_bindir}/dconf
%{_libdir}/libdconf.so.*
%{_libdir}/libdconf-dbus-1.so.*
%{_datadir}/bash-completion/completions/dconf

%files dev
%{_includedir}/dconf
%{_libdir}/libdconf.so
%{_libdir}/pkgconfig/dconf.pc
%{_includedir}/dconf-dbus-1
%{_libdir}/libdconf-dbus-1.so
%{_libdir}/pkgconfig/dconf-dbus-1.pc
%{_datadir}/gtk-doc/html/dconf
%{_datadir}/vala

%changelog
* Mon Nov 24 2014 Alexander Larsson <alexl@redhat.com> - 0.22.0-1
- Initial version, based on F21
