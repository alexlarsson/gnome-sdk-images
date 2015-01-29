%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           at-spi2-atk
Version:        2.15.4
Release:        1%{?dist}
Summary:        A GTK+ module that bridges ATK to D-Bus at-spi

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
#VCS: git:git://git.gnome.org/at-spi-atk
Source0:        http://download.gnome.org/sources/at-spi2-atk/%{release_version}/%{name}-%{version}.tar.xz

BuildRequires:  gnome-sdk-base
BuildRequires:  atk-dev
BuildRequires:  at-spi2-core-dev
BuildRequires:  dbus-dev
BuildRequires:  dbus-glib-dev
BuildRequires:  glib2-dev

Requires:       atk%{?_isa} >= %{atk_version}
Requires:       at-spi2-core%{?_isa} >= %{at_spi2_core_version}

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

This package includes a gtk-module that bridges ATK to the new
D-Bus based at-spi.

%package dev
Summary:        A GTK+ module that bridges ATK to D-Bus at-spi
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description dev
The %{name}-dev package includes the header files for the %{name} library.

%prep
%setup -q

%build
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/libatk-bridge.la
rm $RPM_BUILD_ROOT%{_libdir}/libatk-bridge-2.0.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING AUTHORS README
%dir %{_libdir}/gtk-2.0
%dir %{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/modules/libatk-bridge.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/at-spi2-atk.desktop
%{_libdir}/libatk-bridge-2.0.so.*

%files dev
%{_includedir}/at-spi2-atk/2.0/atk-bridge.h
%{_libdir}/libatk-bridge-2.0.so
%{_libdir}/pkgconfig/atk-bridge-2.0.pc


%changelog
* Wed Nov 12 2014 Alexander Larsson <alexl@redhat.com> - 2.14.1-1
- Initial version based on F21
