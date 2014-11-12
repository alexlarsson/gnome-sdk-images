%define gettext_package dbus

Summary: GLib bindings for D-Bus
Name: dbus-glib
Version: 0.100.2
Release: 1%{?dist}
URL: http://www.freedesktop.org/software/dbus/
#VCS: git:git://git.freedesktop.org/git/dbus/dbus-glib
Source0: http://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
License: AFL and GPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gnome-sdk-base
BuildRequires: dbus-devel
BuildRequires: glib2-devel

%description

D-Bus add-on library to integrate the standard D-Bus library with
the GLib thread abstraction and main loop.

%package devel
Summary: Libraries and headers for the D-Bus GLib bindings
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: glib2-devel
Requires: dbus-devel

%description devel

Headers and static libraries for the D-Bus GLib bindings

%prep
%setup -q

%build
%configure --disable-tests \
	--enable-verbose-mode=yes \
	--enable-asserts=yes \
	--disable-gtk-doc
make

%install
rm -rf %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)

%doc COPYING NEWS

%{_libdir}/*glib*.so.*
%{_bindir}/dbus-binding-tool

%files devel
%defattr(-,root,root)

%{_libdir}/lib*.so
%{_libdir}/pkgconfig/dbus-glib-1.pc
%{_includedir}/dbus-1.0/dbus/*
%{_datadir}/gtk-doc/html/dbus-glib
%{_mandir}/man1/*
%{_sysconfdir}/bash_completion.d/dbus-bash-completion.sh
%{_libexecdir}/dbus-bash-completion-helper

%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 0.100.2-1
- Initial version based on F21
